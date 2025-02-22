"""Internal typing module.

Contains type aliases intended for private use.
"""

from __future__ import annotations

from typing import Any, Literal, TypeAlias

Engine: TypeAlias = Literal["cpu", "gpu"]
PlanTypePreference = Literal["dot", "plain"]

Json: TypeAlias = dict[str, Any]
PlanType: TypeAlias = Literal["physical", "ir"]
FileType: TypeAlias = Literal["none", "parquet", "ipc", "csv", "ndjson", "json"]
