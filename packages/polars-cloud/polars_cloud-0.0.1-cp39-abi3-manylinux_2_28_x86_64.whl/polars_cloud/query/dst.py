from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from polars import ParquetCompression


class ParquetDst:
    def __init__(
        self,
        uri: str | Path,
        *,
        compression: ParquetCompression = "zstd",
        compression_level: int | None = None,
        statistics: bool = True,
        row_group_size: int | None = None,
        data_page_size: int | None = None,
    ) -> None:
        """Parquet destination arguments.

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
        self.uri: str | Path = uri  #: Path to which the output should be written
        self.compression: ParquetCompression = compression  #: Compression algorithm
        self.compression_level: int | None = compression_level  #: Compression level
        self.statistics: bool = statistics  #: Write statistics to parquet headers
        self.row_group_size: int | None = row_group_size  #: Size of the row groups
        self.data_page_size: int | None = data_page_size  #: Data Page size
