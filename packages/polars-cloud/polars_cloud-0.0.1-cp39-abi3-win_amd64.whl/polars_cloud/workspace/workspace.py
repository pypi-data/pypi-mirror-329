from __future__ import annotations

import logging
import time
import webbrowser
from functools import cache
from typing import TYPE_CHECKING
from uuid import UUID

import polars_cloud.polars_cloud as plcr
from polars_cloud.exceptions import VerificationTimeoutError, WorkspaceResolveError
from polars_cloud.workspace.workspace_compute_default import (
    WorkspaceDefaultComputeSpecs,
)
from polars_cloud.workspace.workspace_status import WorkspaceStatus

if TYPE_CHECKING:
    import sys

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self

logger = logging.getLogger(__name__)

POLLING_INTERVAL_SECONDS_DEFAULT = 2
POLLING_TIMEOUT_SECONDS_DEFAULT = 300


class Workspace:
    """Polars Workspace.

    Parameters
    ----------
    name
        Name of the workspace.
    id
        Workspace identifier.
    """

    def __init__(
        self,
        name: str | None = None,
        *,
        id: UUID | None = None,
    ):
        self._name = name
        self._id = id
        self._status: None | WorkspaceStatus = None
        self._defaults: None | WorkspaceDefaultComputeSpecs = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self._id!r}, "
            f"name={self._name!r}, "
            f"status={self._status!r}, "
            f"defaults={self._defaults!r})"
        )

    @classmethod
    def _from_api_schema(cls, workspace_schema: plcr.WorkspaceSchema) -> Self:
        """Parse API result into a Python object."""
        self = cls(
            name=workspace_schema.name,
            id=UUID(workspace_schema.id),
        )
        self._status = WorkspaceStatus._from_api_schema(workspace_schema.status)
        return self

    @property
    def id(self) -> UUID:
        """Workspace id."""
        if self._id is None:
            self.load()
        assert self._id is not None
        return self._id

    @property
    def name(self) -> str:
        """Workspace name."""
        if self._name is None:
            self.load()
        assert self._name is not None
        return self._name

    @property
    def status(self) -> WorkspaceStatus:
        """Workspace status."""
        if self._status is None:
            self.load()
        assert self._status is not None
        return self._status

    @property
    @cache  # noqa: B019
    def defaults(self) -> WorkspaceDefaultComputeSpecs | None:
        """Default Cluster Specification."""
        try:
            self._defaults = WorkspaceDefaultComputeSpecs._from_api_schema(
                plcr.get_workspace_default_compute_specs(str(self.id))
            )
        except plcr.NotFoundError as _:
            self._defaults = None

        return self._defaults

    @defaults.setter
    def defaults(self, value: WorkspaceDefaultComputeSpecs) -> None:
        """Set the default cluster settings of the workspace."""
        plcr.set_workspace_cluster_defaults(
            str(self.id),
            value.cluster_size,
            value.cpus,
            value.memory,
            value.instance_type,
            value.storage,
        )
        self._defaults = value

    @classmethod
    def _parse(cls, workspace: str | Workspace | UUID | None) -> Self:
        """Create a Workspace based on generic user input."""
        if isinstance(workspace, Workspace):
            return workspace  # type: ignore[return-value]
        elif isinstance(workspace, str):
            return cls(name=workspace)
        elif isinstance(workspace, UUID):
            return cls(id=workspace)
        elif workspace is None:
            return cls()
        else:
            msg = f"Unknown type {type(workspace)}, expected str | Workspace | UUID | None"
            raise RuntimeError(msg)

    def load(self) -> None:
        """Load the workspace details (e.g. name, status, id) from the control plane.

        .. note::

         Depending on the input `load` will load the `Workspace` object by id / name
         or if neither is given it will attempt to get the users default workspace.
        """
        if self._id is not None:
            self._load_by_id()
        elif self._name is not None:
            self._load_by_name()
        else:
            self._load_by_default()

    def _load_by_name(self) -> None:
        """Load the workspace by name."""
        workspaces = plcr.list_workspaces(self._name)
        if not workspaces:
            msg = f"Workspace {self._name!r} does not exist"
            raise WorkspaceResolveError(msg)
        elif len(workspaces) == 1:
            workspace_details = workspaces[0]
            self._id = UUID(workspace_details.id)
            self._status = WorkspaceStatus._from_api_schema(workspace_details.status)
        else:
            msg = (
                f"Multiple workspaces with the same name {self._name!r}."
                "\n\nHint: Rename one of your workspaces in the dashboard"
            )
            raise WorkspaceResolveError(msg)

    def _load_by_id(self) -> None:
        """Load the workspace by id."""
        workspace_details = plcr.get_workspace_details(str(self._id))
        self._name = workspace_details.name
        self._status = WorkspaceStatus._from_api_schema(workspace_details.status)

    def _load_by_default(self) -> None:
        """Load the workspace by the default of the user."""
        user: plcr.UserSchema = plcr.get_user()
        if user.default_workspace_id is None:
            msg = (
                "No (default) workspace specified."
                "\n\nHint: Either directly specify the workspace or set your default workspace in the dashboard."
            )
            raise WorkspaceResolveError(msg)
        self._id = UUID(user.default_workspace_id)
        self._load_by_id()

    def is_active(self) -> bool:
        """Whether the Workspace is active."""
        return self.status == WorkspaceStatus.Active

    def verify(
        self,
        *,
        interval: int = POLLING_INTERVAL_SECONDS_DEFAULT,
        timeout: int = POLLING_TIMEOUT_SECONDS_DEFAULT,
    ) -> bool:
        """Verify that a workspace was created correctly.

        Parameters
        ----------
        interval
            The number of seconds between each verification call.
        timeout
            The number of seconds before verification fails.
        """
        max_polls = int(timeout / interval) + 1
        prev_status = WorkspaceStatus.Uninitialized
        logger.debug("polling workspace details endpoint")
        for _ in range(max_polls):
            workspace = Workspace._from_api_schema(
                plcr.get_workspace_details(str(self.id))
            )
            logger.debug("current workspace status: %s", workspace.status)

            if workspace.status != prev_status:
                # Log a message when status changes from UNINITIALIZED to PENDING
                if workspace.status == WorkspaceStatus.Pending:
                    logger.info("workspace stack is being deployed")
                prev_status = workspace.status

            if workspace.status in [
                WorkspaceStatus.Uninitialized,
                WorkspaceStatus.Pending,
            ]:
                time.sleep(interval)
                continue
            elif workspace.status == WorkspaceStatus.Active:
                logger.info("workspace successfully verified")
                return True
            elif workspace.status in [WorkspaceStatus.Failed, WorkspaceStatus.Deleted]:
                logger.info(
                    "workspace verification failed: status is %s", workspace.status
                )
                return False

        else:
            msg = (
                "workspace verification has timed out."
                " Either check the status in your AWS CloudFormation dashboard"
                " or (re-)run workspace verification."
            )
            logger.debug(msg)
            raise VerificationTimeoutError(msg)

    def delete(self) -> None:
        """Delete a workspace."""
        check = input("Are you sure you want to delete the workspace? (y/n)")
        if check not in ["y", "Y"]:
            return
        logger.debug("Calling workspace delete endpoint")
        workspace_info = plcr.delete_workspace(str(self.id))

        if workspace_info is not None:
            logger.debug("opening CloudFormation console")
            _open_cloudformation_console(workspace_info.stack_name, workspace_info.url)
        else:
            print("Successfully deleted workspace")

    @classmethod
    def setup(cls, name: str, *, verify: bool = True) -> Self:
        """Create a new workspace.

        Parameters
        ----------
        name
            Name of the workspace
        verify
            Wait for workspace to become active
        """
        logger.debug("creating workspace")
        workspace_schema = plcr.create_workspace(name)

        logger.debug("opening web browser")
        _open_browser(workspace_schema.url)

        workspace = cls._from_api_schema(workspace_schema.workspace)
        if verify:
            logger.info("verifying workspace creation")
            workspace.verify()

        logger.info("workspace setup successful")
        return workspace

    @classmethod
    def list(cls, name: str | None = None) -> list[Workspace]:
        """List all workspaces the user has access to.

        Parameters
        ----------
        name
            Filter workspaces by name prefix.
        """
        return [cls._from_api_schema(s) for s in plcr.list_workspaces(name)]


def _open_browser(url: str) -> None:
    """Open a web browser for the user at the specified URL."""
    webbrowser.open(url)
    print(
        "Please complete the workspace setup process in your browser.\n"
        "Workspace creation may take up to 5 minutes to complete after clicking 'Create stack'.\n"
        "If your browser did not open automatically, please go to the following URL:\n"
        f"{url}"
    )


def _open_cloudformation_console(stack_name: str, url: str) -> None:
    print(
        f"To delete your workspace, remove the {stack_name} CloudFormation stack in AWS, \n"
        "which will automatically notify Polars Cloud and delete the workspace.\n"
        "This action will delete all resources associated with your workspace.\n"
        "You will be redirected to the AWS CloudFormation console in 5 seconds to complete the process."
    )
    time.sleep(5)
    webbrowser.open(url)
