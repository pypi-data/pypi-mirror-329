from __future__ import annotations

from typing import TYPE_CHECKING

from polars import LazyFrame

from polars_cloud.query.dst import ParquetDst
from polars_cloud.query.query import spawn

if TYPE_CHECKING:
    from pathlib import Path

    from polars import ParquetCompression

    from polars_cloud._typing import PlanTypePreference
    from polars_cloud.context import ComputeContext
    from polars_cloud.query.query import BatchQuery, InteractiveQuery


class LazyFrameExt:
    def __init__(
        self,
        lf: LazyFrame,
        context: ComputeContext | None = None,
        plan_type: PlanTypePreference = "dot",
    ) -> None:
        self.lf: LazyFrame = lf
        self.context: ComputeContext | None = context
        self._partition_by: None | str | list[str] = None
        self._broadcast_over: None | list[list[list[Path]]] = None
        self._distributed: None | bool = None
        self._labels: None | list[str] = None
        self.plan_type: PlanTypePreference = plan_type

    def __check_partition_by_broadcast_over(self) -> None:
        if self._broadcast_over is not None and self._partition_by is not None:
            msg = "only 1 of 'partition_by' or 'broadcast_over' can be set"
            raise ValueError(msg)

    def distributed(self) -> LazyFrameExt:
        """Whether the query should run in a distributed fashion."""
        self._distributed = True
        return self

    def labels(self, labels: list[str] | str) -> LazyFrameExt:
        """Add labels to the query.

        Parameters
        ----------
        labels
            Labels to add to the query (will be implicitly created)
        """
        self._labels = [labels] if isinstance(labels, str) else labels
        return self

    def partition_by(self, key: str | list[str]) -> LazyFrameExt:
        """Partition this query by the given key.

        This first partitions the data by the key and then runs this query
        per unique key. This will lead to ``N`` output results, where ``N``
        is equal to the number of unique values in ``key``

        This will run on multiple workers.

        Parameters
        ----------
        key
            Key/keys to partition over.

        """
        self._partition_by = key
        self.__check_partition_by_broadcast_over()
        return self

    def broadcast_over(self, over: list[list[list[Path]]]) -> LazyFrameExt:
        """Run this queries in parallel over the given source paths.

        This will run on multiple workers.

        Parameters
        ----------
        over
            Run this queries in parallel over the given source paths.

            Levels from outer to inner:
            1 -> partition paths
            2 -> src in DSL
            3 -> paths (plural) in a single DSL source.

        """
        self._broadcast_over = over
        self.__check_partition_by_broadcast_over()
        return self

    def sink_parquet(
        self,
        uri: str,
        *,
        compression: ParquetCompression = "zstd",
        compression_level: int | None = None,
        statistics: bool = True,
        row_group_size: int | None = None,
        data_page_size: int | None = None,
    ) -> InteractiveQuery | BatchQuery:
        """Start executing the query and write the result to parquet.

        Parameters
        ----------
        uri
            Path to which the output should be written.
            Must be a URI to an accessible object store location.
            If set to `"local"`, the query is executed locally.
        compression : {'lz4', 'uncompressed', 'snappy', 'gzip', 'lzo', 'brotli', 'zstd'}
            Choose "zstd" for good compression performance.
            Choose "lz4" for fast compression/decompression.
            Choose "snappy" for more backwards compatibility guarantees
            when you deal with older parquet readers.
        compression_level
            The level of compression to use. Higher compression means smaller files on
            disk.

            - "gzip" : min-level: 0, max-level: 10.
            - "brotli" : min-level: 0, max-level: 11.
            - "zstd" : min-level: 1, max-level: 22.

        statistics
            Write statistics to the parquet headers. This is the default behavior.
        row_group_size
            Size of the row groups in number of rows. Defaults to 512^2 rows.
        data_page_size
            Size of the data page in bytes. Defaults to 1024^2 bytes.

        """
        dst = ParquetDst(
            uri=uri,
            compression=compression_level,
            compression_level=compression_level,
            statistics=statistics,
            row_group_size=row_group_size,
            data_page_size=data_page_size,
        )

        return spawn(
            lf=self.lf,
            dst=dst,
            context=self.context,
            partitioned_by=self._partition_by,
            broadcast_over=self._broadcast_over,
            plan_type=self.plan_type,
            distributed=self._distributed,
            labels=self._labels,
        )


def remote(
    lf: LazyFrame,
    context: ComputeContext | None = None,
    plan_type: PlanTypePreference = "dot",
) -> LazyFrameExt:
    return LazyFrameExt(lf, context=context, plan_type=plan_type)


# TODO: For typing reasons this will be done in Polars
# when we have released polars-cloud
LazyFrame.remote = remote  # type: ignore[attr-defined]
