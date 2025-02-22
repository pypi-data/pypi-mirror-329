from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING
from uuid import UUID

import polars_cloud.polars_cloud as plcr
from polars_cloud.context.compute_specs import resolve_compute_context_specs
from polars_cloud.context.compute_status import ComputeContextStatus
from polars_cloud.workspace import Workspace

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    import sys

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

SCHEDULER_PORT = 5051


class ComputeContext:
    """Compute context in which queries are executed.

    The compute context is an abstraction of the underlying hardware
    (either a single node or multiple nodes in case of a cluster).

    Parameters
    ----------
    cpus
        The minimum number of CPUs the compute context should have access to.
    memory
        The minimum amount of RAM (in GB) the compute context should have access to.
    instance_type
        The instance type to use.
    storage
        The minimum amount of disk space (in GB) the compute context should have access
        to.
    cluster_size
        The number of machines to spin up in the cluster. Defaults to `1`.
    interactive
        Whether to compute context should run in interactive mode. Defaults to `False`.
    workspace
        The workspace to run this context in.
        You may specify the name (str), the id (UUID) or the Workspace object.
    labels
        Labels of the workspace (will be implicitly created)
    log_level
        Override the log level of the context for debug purposes.
        One of `"info", "debug", "trace"`.


    Notes
    -----
    .. note::
     If the `cpus`, `memory`, and `instance_type` parameters are not set, the parameters
     are resolved with the default context specs of the workspace.
    """

    def __init__(
        self,
        *,
        cpus: int | None = None,
        memory: int | None = None,
        instance_type: str | None = None,
        storage: int | None = None,
        cluster_size: int | None = None,
        interactive: bool = False,
        workspace: str | UUID | Workspace | None = None,
        labels: list[str] | str | None = None,
        log_level: plcr.LogLevelSchema | None = None,
    ) -> None:
        self._workspace = Workspace._parse(workspace)
        self._specs = resolve_compute_context_specs(
            self._workspace,
            cpus=cpus,
            memory=memory,
            instance_type=instance_type,
            storage=storage,
            cluster_size=cluster_size,
        )

        self._labels = [labels] if isinstance(labels, str) else labels
        self._interactive = interactive
        self._compute_id: UUID | None = None
        self._compute_address: str | None = None
        self._compute_public_key: bytes | None = None
        self._log_level = log_level

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self._compute_id}, "
            f"cpus={self._specs.cpus!r}, "
            f"memory={self._specs.memory!r}, "
            f"instance_type={self._specs.instance_type!r}, "
            f"storage={self._specs.storage!r}, "
            f"cluster_size={self._specs.cluster_size!r}, "
            f"interactive={self.interactive!r}, "
            f"workspace_name={self.workspace.name!r}, "
            f"labels={self.labels!r}, "
            f"log_level={self._log_level!r})"
        )

    @classmethod
    def _from_api_schema(cls, schema: plcr.ComputeSchema) -> Self:
        self = cls(
            cpus=schema.req_cpu_cores,
            memory=schema.req_ram_gb,
            cluster_size=schema.cluster_size,
            instance_type=schema.instance_type,
            storage=schema.req_storage,
            workspace=Workspace(id=UUID(schema.workspace_id)),
            interactive=schema.mode == plcr.DBClusterModeSchema.Interactive,
            # TODO: Get the labels as well
            labels=None,
            # TODO: Persist the loglevel
            log_level=None,
        )
        self._compute_id = UUID(schema.id)
        return self

    def get_status(self) -> ComputeContextStatus:
        """Get the status of the compute context."""
        if self._compute_id is None:
            return ComputeContextStatus.UNINITIALIZED
        else:
            status = plcr.get_compute_status(
                str(self.workspace.id), str(self._compute_id)
            )
            return ComputeContextStatus._from_api_schema(status)

    def start(self, *, wait: bool = False) -> None:
        """Start the compute context.

        This boots up the underlying node(s) of the compute context.

        Parameters
        ----------
        wait
            Wait for the context to be ready before returning.
            If in interactive mode, always True.
        """
        if self._compute_id is not None:
            msg = "the context is already running"
            raise RuntimeError(msg)

        wait = True if self.interactive else wait

        if self.interactive:
            mode = plcr.DBClusterModeSchema.Interactive
        else:
            mode = plcr.DBClusterModeSchema.Batch

        str_id = plcr.start_compute(
            workspace_id=str(self.workspace.id),
            cluster_size=self._specs.cluster_size,
            mode=mode,
            cpus=self._specs.cpus,
            ram_gb=self._specs.memory,
            instance_type=self._specs.instance_type,
            storage=self._specs.storage,
            labels=self._labels,
            log_level=self.log_level,
        )
        self._compute_id = UUID(str_id)
        if wait:
            _poll_compute_status_until(self, ComputeContextStatus.RUNNING)

        if self.interactive:
            self._get_server_info()

    def stop(self, *, wait: bool = False) -> None:
        """Stop the compute context.

        Parameters
        ----------
        wait
            Wait for the context to be stopped.
        """
        if self._compute_id is None:
            msg = "nothing to stop, context is not running"
            raise RuntimeError(msg)

        plcr.stop_compute(str(self.workspace.id), str(self._compute_id))
        if wait:
            _poll_compute_status_until(self, ComputeContextStatus.STOPPED, 10, 5, 100)

        self._compute_id = None
        self._compute_address = None
        self._compute_public_key = None

    @classmethod
    def list(cls, workspace_id: UUID) -> list[Self]:
        """List all compute contexts in the workspace."""
        compute_contexts = plcr.list_compute(str(workspace_id))
        return [cls._from_api_schema(c) for c in compute_contexts]

    @classmethod
    def connect(cls, workspace_id: UUID, compute_id: UUID) -> Self:
        """Reconnect with an already running compute context.

        Parameters
        ----------
        workspace_id
            The identifier of the Workspace
        compute_id
            The unique identifier of the existing compute context.
        """
        details = plcr.get_compute_details(str(workspace_id), str(compute_id))
        ctx = cls._from_api_schema(details)
        status = ctx.get_status()
        if not status.is_available():
            msg = f"Context is in an incorrect state: {status}"
            raise RuntimeError(msg)
        return ctx

    @property
    def cpus(self) -> int | None:
        """The number of CPUs the compute context has access to."""
        return self._specs.cpus

    @property
    def memory(self) -> int | None:
        """The amount of RAM (in GB) the compute context has access to."""
        return self._specs.memory

    @property
    def instance_type(self) -> str | None:
        """The instance type of the compute context."""
        return self._specs.instance_type

    @property
    def storage(self) -> int | None:
        """The amount of disk space (in GB) the compute context has access to."""
        return self._specs.storage

    @property
    def cluster_size(self) -> int:
        """The number of compute nodes in the context."""
        return self._specs.cluster_size

    @property
    def interactive(self) -> bool:
        """Whether the compute context runs in interactive mode."""
        return self._interactive

    @property
    def labels(self) -> list[str] | None:  # type: ignore[valid-type]
        """The labels of the compute context."""
        return self._labels

    @property
    def workspace(self) -> Workspace:
        """The workspace to run the compute context in."""
        return self._workspace

    @property
    def log_level(self) -> plcr.LogLevelSchema | None:
        return self._log_level

    @property
    def compute_address(self) -> str | None:
        if not self.interactive:
            return None
        else:
            if self._compute_address is None:
                self._get_server_info()
            return self._compute_address

    @property
    def compute_public_key(self) -> bytes | None:
        if not self.interactive:
            return None
        else:
            if self._compute_address is None:
                self._get_server_info()
            return self._compute_public_key

    def _get_server_info(self) -> None:
        logger.debug("Getting compute server info")
        server_info = plcr.get_compute_server_info(
            str(self.workspace.id), str(self._compute_id)
        )
        self._compute_address = f"{server_info.public_address}:{SCHEDULER_PORT}"
        self._compute_public_key = str.encode(server_info.public_server_key)
        logger.debug("Successfully obtained compute server info")


def _poll_compute_status_until(
    compute: ComputeContext,
    desired_state: ComputeContextStatus,
    start_delay: int = 60,
    interval: int = 3,
    timeout: int = 300,
) -> ComputeContextStatus:
    """Poll the compute status until the compute context is in desired_state."""
    max_polls = int((timeout - start_delay) / interval)
    time.sleep(start_delay)
    for i in range(max_polls):
        logger.debug("Polling compute status (try %s)", str(i))
        status = compute.get_status()
        logging.debug("Got compute status %s", status)
        if status == desired_state:
            return status
        elif status == ComputeContextStatus.FAILED:
            msg = "Compute cluster in failed state"
            logger.info(msg)
            raise RuntimeError(msg)
        else:
            time.sleep(interval)
    else:
        msg = f"Compute context failed to reach desired state {desired_state} after polling for {timeout} seconds"
        logger.info(msg)
        raise RuntimeError(msg)
