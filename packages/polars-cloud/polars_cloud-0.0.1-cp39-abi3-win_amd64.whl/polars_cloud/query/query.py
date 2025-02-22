from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from time import sleep
from typing import TYPE_CHECKING
from uuid import UUID

import polars as pl

# needed for eval
from polars.exceptions import (  # noqa: F401
    ColumnNotFoundError,
    ComputeError,
    DuplicateError,
    InvalidOperationError,
    NoDataError,
    SchemaError,
    SchemaFieldNotFoundError,
    ShapeError,
    SQLSyntaxError,
    StringCacheMismatchError,
    StructFieldNotFoundError,
)

import polars_cloud.polars_cloud as plcr
from polars_cloud._utils import run_coroutine
from polars_cloud.context import ComputeContext
from polars_cloud.context import cache as compute_cache
from polars_cloud.query._utils import prepare_query
from polars_cloud.query.query_info import QueryInfo
from polars_cloud.query.query_result import QueryResult
from polars_cloud.query.query_status import QueryStatus

if TYPE_CHECKING:
    from pathlib import Path

    from polars import LazyFrame

    from polars_cloud._typing import Engine, PlanTypePreference
    from polars_cloud.query.dst import ParquetDst


# Not to be mistaken with `polars.InprogressQuery` which is local
class InProgressQueryRemote(ABC):
    """Abstract base class for an in progress remote query."""

    @abstractmethod
    def get_status(self) -> QueryStatus:
        """Get the current status of the query."""

    @abstractmethod
    async def await_result_async(self, *, raise_on_failure: bool = True) -> QueryResult:
        """Await the result of the query asynchronously and return the result."""

    @abstractmethod
    def await_result(self, *, raise_on_failure: bool = True) -> QueryResult:
        """Block the current thread until the query is processed and get a result."""

    @abstractmethod
    def cancel(self) -> None:
        """Cancel the execution of the query."""

    async def _poll_status_until_done_async(self) -> QueryStatus:
        """Poll the status of the query until it is either completed or failed."""
        i = 0
        # while in_progress(status := self.get_status()):
        while not (status := self.get_status()).is_done():
            i += 1
            await asyncio.sleep(min(1, 0.05 * 1.5 ** min(30, i)))

        return status

    def _poll_status_until_done(self) -> QueryStatus:
        """Poll the status of the query until it is either completed or failed."""
        i = 0
        while not (status := self.get_status()).is_done():
            i += 1
            sleep(min(1, 0.05 * 1.5 ** min(30, i)))

        return status


class BatchQuery(InProgressQueryRemote):
    """A Polars Cloud batch query.

    .. note::
     This object is returned when spawning a new query on a compute cluster running
     in batch mode. It should not be instantiated directly by the user.
    """

    def __init__(self, query_id: UUID, workspace_id: UUID):
        self._query_id = query_id
        self._workspace_id = workspace_id

    def get_status(self) -> QueryStatus:
        schema = plcr.get_query(str(self._workspace_id), str(self._query_id))
        query_status = QueryStatus._from_api_schema(schema.status.code)
        return query_status

    def _get_result(
        self, status: QueryStatus, *, raise_on_failure: bool = True
    ) -> QueryResult:
        result_raw = plcr.get_query_result(str(self._query_id))
        result = QueryResult(
            result=QueryInfo(id=self._query_id, inner=result_raw), status=status
        )

        if raise_on_failure and status == QueryStatus.FAILED:
            result.raise_err()

        return result

    async def await_result_async(self, *, raise_on_failure: bool = True) -> QueryResult:
        status = await self._poll_status_until_done_async()
        return self._get_result(status, raise_on_failure=raise_on_failure)

    def await_result(self, *, raise_on_failure: bool = True) -> QueryResult:
        status = self._poll_status_until_done()
        return self._get_result(status, raise_on_failure=raise_on_failure)

    def cancel(self) -> None:
        plcr.cancel_batch_query(
            workspace_id=str(self._workspace_id), query_id=str(self._query_id)
        )


class InteractiveQuery(InProgressQueryRemote):
    """A Polars Cloud interactive query.

    .. note::
     This object is returned when spawning a new query on a compute cluster running
     in interactive mode. It should not be instantiated directly by the user.
    """

    def __init__(self, query_id: UUID, address: str, public_key: bytes):
        self._query_id = query_id
        self._address = address
        self._public_key = public_key

    def get_status(self) -> QueryStatus:
        status_code = plcr.get_interactive_query_status(
            self._address,
            str(self._query_id),
            self._public_key,
        )
        return QueryStatus._from_proto(status_code)

    def _get_result(
        self, status: QueryStatus, *, raise_on_failure: bool = True
    ) -> QueryResult:
        query_info_py = plcr.get_interactive_query_result(
            self._address,
            str(self._query_id),
            self._public_key,
        )
        query_info = QueryInfo(self._query_id, query_info_py)
        result = QueryResult(result=query_info, status=status)

        if raise_on_failure and status == QueryStatus.FAILED:
            result.raise_err()

        return result

    async def await_result_async(self, *, raise_on_failure: bool = True) -> QueryResult:
        status = await self._poll_status_until_done_async()
        return self._get_result(status, raise_on_failure=raise_on_failure)

    def await_result(self, *, raise_on_failure: bool = True) -> QueryResult:
        status = self._poll_status_until_done()
        return self._get_result(status, raise_on_failure=raise_on_failure)

    def cancel(self) -> None:
        """Cancel the query."""
        plcr.cancel_interactive_query(
            self._address,
            str(self._query_id),
            self._public_key,
        )


def spawn_many(
    lf: list[LazyFrame],
    *,
    dst: Path | str | ParquetDst,
    context: ComputeContext | None = None,
    distributed: None | bool = None,
    engine: Engine = "cpu",
    plan_type: PlanTypePreference = "dot",
    **optimizations: bool,
) -> list[BatchQuery] | list[InteractiveQuery]:
    """Spawn a multiple remote queries and await it asynchronously.

    Parameters
    ----------
    lf
        A list of Polars LazyFrame's which should be executed on the compute cluster.
    dst
        Destination to which the output should be written.
        If an URI is passed, it must be an accessible object store location.
        If set to `"local"`, the query is executed locally.
    context
        The context describing the compute cluster that should execute the query.
        If set to `None` (default), attempts to load a valid compute context from the
        following locations in order:

        1. The compute context cache. This contains the last `Compute` context created.
        2. The default compute context stored in the user profile.
    distributed
        Run as as distributed query. This may run partially distributed, depending
        on the operation, optimizer statistics and available machines.
    engine : {'cpu', 'gpu'}
        Execute the query with either the CPU or the GPU.
        Setting the engine to GPU requires the compute cluster to have access to GPUs.
        If it does not, the query will fail.
    plan_type: {"dot", "plain"}
        Which output format is preferred.
    **optimizations
        Optimizations to enable or disable in the query optimizer, e.g.
        `projection_pushdown=False`.

    Raises
    ------
    grpc.RpcError
        If the LazyFrame size is too large. See note below.
    """
    return [  # type: ignore[return-value]
        spawn(
            lf_,
            dst=dst,
            context=context,
            distributed=distributed,
            engine=engine,
            plan_type=plan_type,
            **optimizations,  # type: ignore[arg-type]
        )
        for lf_ in lf
    ]


def spawn_many_blocking(
    lf: list[LazyFrame],
    *,
    dst: Path | str | ParquetDst,
    context: ComputeContext | None = None,
    distributed: None | bool = None,
    engine: Engine = "cpu",
    plan_type: PlanTypePreference = "dot",
    **optimizations: bool,
) -> list[QueryResult]:
    """Spawn a multiple remote queries and await it asynchronously.

    Parameters
    ----------
    lf
        A list of Polars LazyFrame's which should be executed on the compute cluster.
    dst
        Destination to which the output should be written.
        If an URI is passed, it must be an accessible object store location.
        If set to `"local"`, the query is executed locally.
    context
        The context describing the compute cluster that should execute the query.
        If set to `None` (default), attempts to load a valid compute context from the
        following locations in order:

        1. The compute context cache. This contains the last `Compute` context created.
        2. The default compute context stored in the user profile.
    distributed
        Run as as distributed query. This may run partially distributed, depending
        on the operation, optimizer statistics and available machines.
    engine : {'cpu', 'gpu'}
        Execute the query with either the CPU or the GPU.
        Setting the engine to GPU requires the compute cluster to have access to GPUs.
        If it does not, the query will fail.
    plan_type: {"dot", "plain"}
        Which output format is preferred.
    **optimizations
        Optimizations to enable or disable in the query optimizer, e.g.
        `projection_pushdown=False`.

    Raises
    ------
    grpc.RpcError
        If the LazyFrame size is too large. See note below.
    """

    async def run() -> list[QueryResult]:
        in_process = spawn_many(
            lf,
            dst=dst,
            distributed=distributed,
            context=context,
            engine=engine,
            plan_type=plan_type,
            **optimizations,
        )
        tasks = [asyncio.create_task(t.await_result_async()) for t in in_process]
        return await asyncio.gather(*tasks)

    return run_coroutine(run())


def spawn(
    lf: LazyFrame,
    *,
    dst: Path | str | ParquetDst,
    context: ComputeContext | None = None,
    distributed: None | bool = None,
    partitioned_by: None | str | list[str] = None,
    broadcast_over: None | list[list[list[Path]]] = None,
    engine: Engine = "cpu",
    plan_type: PlanTypePreference = "dot",
    labels: None | list[str] = None,
    **optimizations: bool,
) -> BatchQuery | InteractiveQuery:
    """Spawn a remote query and await it asynchronously.

    Parameters
    ----------
    lf
        The Polars LazyFrame which should be executed on the compute cluster.
    dst
        Destination to which the output should be written.
        If an URI is passed, it must be an accessible object store location.
        If set to `"local"`, the query is executed locally.
    context
        The context describing the compute cluster that should execute the query.
        If set to `None` (default), attempts to load a valid compute context from the
        following locations in order:

        1. The compute context cache. This contains the last `Compute` context created.
        2. The default compute context stored in the user profile.
    distributed
        Run as as distributed query. This may run partially distributed, depending
        on the operation, optimizer statistics and available machines.
    partitioned_by
        Partition query by a key
    broadcast_over
        Run this queries in parallel over the given source paths.
    engine : {'cpu', 'gpu'}
        Execute the query with either the CPU or the GPU.
        Setting the engine to GPU requires the compute cluster to have access to GPUs.
        If it does not, the query will fail.
    plan_type: {"dot", "plain"}
        Which output format is preferred.
    labels
        Labels to add to the query (will be implicitly created)
    **optimizations
        Optimizations to enable or disable in the query optimizer, e.g.
        `projection_pushdown=False`.

    Raises
    ------
    grpc.RpcError
        If the LazyFrame size is too large. See note below.
    """
    if not isinstance(lf, pl.LazyFrame):
        msg = f"expected a 'LazyFrame' for 'lf', got {type(lf)}"
        raise TypeError(msg)

    # Set compute context if not given
    if context is None:
        if compute_cache.cached_context is not None:
            context = compute_cache.cached_context
        else:
            context = ComputeContext()

    # Start cluster if it is not yet started
    if not context.get_status().is_available():
        context.start()

    plan, settings = prepare_query(
        lf=lf,
        dst=dst,
        partition_by=partitioned_by,
        broadcast_over=broadcast_over,
        engine=engine,
        distributed=distributed,
        plan_type=plan_type,
        **optimizations,
    )
    if context.interactive:
        address: str = context.compute_address  # type: ignore[assignment]
        public_key: bytes = context.compute_public_key  # type: ignore[assignment]
        q_id = plcr.do_query(
            address=address,
            plan=plan,
            settings=settings,
            public_server_cert=public_key,
        )
        return InteractiveQuery(UUID(q_id), address=address, public_key=public_key)
    else:
        q_id = plcr.submit_query(str(context._compute_id), plan, settings, labels)
        return BatchQuery(UUID(q_id), workspace_id=context.workspace.id)


def spawn_blocking(
    lf: LazyFrame,
    *,
    dst: Path | str | ParquetDst,
    context: ComputeContext | None = None,
    distributed: None | bool = None,
    partitioned_by: None | str | list[str] = None,
    broadcast_over: None | list[list[list[Path]]] = None,
    engine: Engine = "cpu",
    plan_type: PlanTypePreference = "dot",
    labels: None | list[str] = None,
    **optimizations: bool,
) -> QueryResult:
    """Spawn a remote query and block the thread until the result is ready.

    Parameters
    ----------
    lf
        The Polars LazyFrame which should be executed on the compute cluster.
    dst
        Destination to which the output should be written.
        If an URI is passed, it must be an accessible object store location.
        If set to `"local"`, the query is executed locally.
    context
        The context describing the compute cluster that should execute the query.
        If set to `None` (default), attempts to load a valid compute context from the
        following locations in order:

        1. The compute context cache. This contains the last `Compute` context created.
        2. The default compute context stored in the user profile.
    distributed
        Run as as distributed query. This may run partially distributed, depending
        on the operation, optimizer statistics and available machines.
    partitioned_by
        Partition query by a key
    broadcast_over
        Run this queries in parallel over the given source paths.
    engine : {'cpu', 'gpu'}
        Execute the query with either the CPU or the GPU.
        Setting the engine to GPU requires the compute cluster to have access to GPUs.
        If it does not, the query will fail.
    plan_type: {"dot", "plain"}
        Which output format is preferred.
    labels
        Labels to add to the query (will be implicitly created)
    **optimizations
        Optimizations to enable or disable in the query optimizer, e.g.
        `projection_pushdown=False`.

    Raises
    ------
    grpc.RpcError
        If the LazyFrame size is too large. See note below.
    """
    in_process = spawn(
        lf,
        dst=dst,
        context=context,
        distributed=distributed,
        partitioned_by=partitioned_by,
        broadcast_over=broadcast_over,
        engine=engine,
        plan_type=plan_type,
        labels=labels,
        **optimizations,
    )
    return in_process.await_result()
