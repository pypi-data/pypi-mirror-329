import sys
from enum import Enum
from typing import final

import polars_cloud.polars_cloud as plcr

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


@final
class ComputeContextStatus(Enum):
    """The status of the compute cluster associated with a `ComputeContext`."""

    UNINITIALIZED = 0
    """Compute Context is not yet initialized with the control plane."""

    STARTING = 1
    """Compute Context is starting."""

    RUNNING = 2
    """Compute Context is running."""

    STOPPING = 3
    """Compute Context is stopping."""

    STOPPED = 4
    """Compute Context stopped."""

    FAILED = 5
    """Compute Context failed."""

    FAILED_BOOT = 6
    """Compute Context failed during boot."""

    FAILED_INFRA = 7
    """Compute Context failed to provision infrastructure."""

    def is_available(self) -> bool:
        return self in [
            ComputeContextStatus.STARTING,
            ComputeContextStatus.RUNNING,
        ]

    @classmethod
    def _from_api_schema(cls, status: plcr.ComputeStatusSchema) -> Self:
        if status == plcr.ComputeStatusSchema.Starting:
            return cls.STARTING
        elif status == plcr.ComputeStatusSchema.Running:
            return cls.RUNNING
        elif status == plcr.ComputeStatusSchema.Stopping:
            return cls.STOPPING
        elif status == plcr.ComputeStatusSchema.Stopped:
            return cls.STOPPED
        elif status == plcr.ComputeStatusSchema.Failed:
            return cls.FAILED
        elif status == plcr.ComputeStatusSchema.FailedBoot:
            return cls.FAILED_BOOT
        elif status == plcr.ComputeStatusSchema.FailedInfra:
            return cls.FAILED_INFRA

    def __repr__(self) -> str:
        return self.name
