import typing
from datetime import datetime
from enum import Enum
from pathlib import Path

from polars_cloud._typing import FileType

def get_auth_header() -> str: ...
def serialize_query_settings(
    *,
    dst: typing.Any,
    max_threads: int | None,
    use_gpu: bool,
    partition_by: list[str] | None = ...,
    broadcast_over: list[list[list[Path]]] | None = ...,
    distributed: bool | None = ...,
    prefer_dot: bool = ...,
) -> bytes: ...

class WorkspaceStateSchema(Enum):
    """Represents the state of a workspace."""

    Uninitialized: int
    Pending: int
    Active: int
    Failed: int
    Deleted: int

class WorkspaceSchema:
    """Represents a workspace schema."""

    id: str
    """Workspace ID (UUID v7)."""

    name: str
    """Workspace Name."""

    description: str
    """Workspace Description."""

    user_id: str
    """User who created the Workspace."""

    status: WorkspaceStateSchema
    """Status of the Workspace."""

    created_at: datetime
    """Creation timestamp."""

    updated_at: datetime
    """Last update timestamp."""

    deleted_at: datetime | None
    """Timestamp of the last deletion."""

    def __init__(self, id: str, name: str, status: WorkspaceStateSchema) -> None: ...

class DefaultComputeSpecs:
    """Represents the default compute specifications."""

    instance_type: str | None
    """The type of instance (e.g., t2.micro)."""

    cpus: int | None
    """Number of CPUs."""

    ram_gb: int | None
    """Amount of RAM in GiB."""

    storage: int | None
    """Amount of disk storage in GiB."""

    cluster_size: int
    """Number of compute nodes."""

def list_workspaces(name: str | None = None) -> list[WorkspaceSchema]: ...
def get_workspace_details(workspace_id: str) -> WorkspaceSchema: ...
def get_workspace_default_compute_specs(workspace_id: str) -> DefaultComputeSpecs: ...
def set_workspace_cluster_defaults(
    workspace_id: str,
    cluster_size: int,
    cpus: int | None,
    memory: int | None,
    instance_type: str | None,
    storage: int | None,
) -> None: ...
def delete_workspace_cluster_defaults(workspace_id: str) -> None: ...

class QuerySchema:
    """Represents the schema for a query."""

    id: str
    """Query ID."""

    workspace_id: str
    """The workspace the query is being run in."""

    cluster_id: str
    """The virtual machine it is sent to."""

    user_id: str
    """The user account that started the instance."""

    request_time: datetime
    """The time the query was requested."""

    created_at: datetime
    """Creation timestamp."""

    updated_at: datetime
    """Last update timestamp."""

    deleted_at: datetime | None
    """Timestamp of the last deletion."""

class QueryStatusCodeSchema(Enum):
    """Represents the status codes for a query."""

    Queued: int
    Scheduled: int
    InProgress: int
    Success: int
    Failed: int
    Canceled: int

class TaskStatusType(Enum):
    Waiting: int
    InProgress: int
    Success: int
    Failed: int
    Canceled: int

class StatusSchema:
    """Represents the status information for a query."""

    status_time: datetime
    """Start time for the status."""

    code: QueryStatusCodeSchema
    """Status code."""

class QueryWithStatusSchema:
    """Represents a query with its associated status."""

    query: QuerySchema
    """Details of the query."""

    status: StatusSchema
    """Current status of the query"""

def list_queries(workspace_id: str) -> list[QueryWithStatusSchema]: ...
def get_query(workspace_id: str, query_id: str) -> QueryWithStatusSchema: ...

class TerminationReasonSchema(Enum):
    """Enum representing the reasons for termination."""

    StoppedByUser: int
    """The instance was stopped by the user."""

    StoppedInactive: int
    """The instance was stopped due to inactivity."""

    Failed: int
    """The instance failed."""

class TerminationSchema:
    """Represents the termination details of a compute instance."""

    termination_reason: TerminationReasonSchema
    """Reason for termination."""

    termination_time: datetime
    """Timestamp when termination occurred."""

    termination_message: str | None
    """Optional message providing details about the termination."""

class DBClusterModeSchema(Enum):
    Batch: int
    Interactive: int

class ComputeSchema:
    """Represents the schema for a compute instance."""

    id: str
    """Unique identifier for the compute instance."""

    user_id: str
    """ID of the user associated with the compute instance."""

    workspace_id: str
    """ID of the workspace the compute instance belongs to."""

    instance_type: str | None
    """Type of instance (e.g., instance type string)."""

    req_ram_gb: int | None
    """Requested RAM in GiB."""

    req_cpu_cores: int | None
    """Requested number of CPU cores."""

    req_storage: int | None
    """Requested disk storage in GiB."""

    cluster_size: int
    """Number of compute nodes in the cluster."""

    termination: TerminationSchema | None
    """Termination settings, if applicable."""

    gc_inactive_hours: int
    """Number of hours before garbage collection of inactive instances."""

    request_time: datetime
    """Timestamp when the compute instance was requested."""

    mode: DBClusterModeSchema
    """Mode of the database cluster."""

    created_at: datetime
    """Timestamp when the compute instance was created."""

    updated_at: datetime
    """Timestamp when the compute instance was last updated."""

    deleted_at: datetime | None
    """Timestamp when the compute instance was deleted, if applicable."""

class LogLevelSchema(Enum):
    """Log level for a compute cluster."""

    Info: int
    Debug: int
    Trace: int

class ComputeClusterPublicInfoSchema:
    cluster_id: str
    public_address: str
    public_server_key: str

class ComputeStatusSchema(Enum):
    Starting: int
    Running: int
    Stopping: int
    Stopped: int
    FailedInfra: int
    FailedBoot: int
    Failed: int

def list_compute(workspace_id: str) -> list[ComputeSchema]: ...
def get_compute_details(workspace_id: str, compute_id: str) -> ComputeSchema: ...
def get_compute_server_info(
    workspace_id: str, compute_id: str
) -> ComputeClusterPublicInfoSchema: ...
def start_compute(
    workspace_id: str,
    cluster_size: int,
    mode: DBClusterModeSchema,
    cpus: int | None,
    ram_gb: int | None,
    instance_type: str | None,
    storage: int | None,
    labels: list[str] | None,
    log_level: LogLevelSchema | None,
) -> str: ...
def stop_compute(
    workspace_id: str,
    compute_id: str,
) -> None: ...
def get_compute_status(
    workspace_id: str,
    compute_id: str,
) -> ComputeStatusSchema: ...

class WorkspaceWithUrlSchema:
    workspace: WorkspaceSchema
    url: str

class WorkspaceSetupUrlSchema:
    setup_url: str
    template_url: str

class DeleteWorkspaceSchema:
    stack_name: str
    url: str

def create_workspace(
    name: str,
) -> WorkspaceWithUrlSchema: ...
def get_workspace_setup_url(workspace_id: str) -> WorkspaceSetupUrlSchema: ...
def delete_workspace(workspace_id: str) -> DeleteWorkspaceSchema | None: ...
def get_workspace_delete_url(workspace_id: str) -> DeleteWorkspaceSchema: ...
def get_user() -> UserSchema: ...

class UserSchema:
    id: str
    """User id."""
    first_name: str | None
    """First name."""
    last_name: str | None
    """Last name."""
    avatar_url: str | None
    """Avatar url."""
    default_workspace_id: str | None
    """The default workspace id (if None specified)."""
    newsletter_updates: bool
    """Whether to receive newsletter updates."""
    personal_emails: bool
    """Whether to receive personal updates."""

class NotFoundError(Exception):
    """Exception raised when a resource is not found."""

class AuthLoadError(Exception):
    """Exception raised when a no authentication could be loaded."""

class QueryInfoPy:
    total_stages: int
    finished_stages: int
    failed_stages: int
    head: bytes | None
    n_rows_result: int | None
    errors: list[str]
    sink_dst: list[str]
    file_type_sink: FileType
    ir_plan_explain: str | None
    ir_plan_dot: str | None
    phys_plan_explain: str | None

def deserialize_query_result(
    payload: typing.Any,
) -> QueryInfoPy: ...
def get_query_result(query_id: str) -> QueryInfoPy: ...
def submit_query(
    compute_id: str, plan: bytes, settings: bytes, labels: list[str] | None
) -> str: ...
def cancel_interactive_query(
    address: str,
    query_id: str,
    public_server_cert: bytes,
) -> None: ...
def cancel_batch_query(
    workspace_id: str,
    query_id: str,
) -> None: ...
def get_interactive_query_result(
    address: str,
    query_id: str,
    public_server_cert: bytes,
) -> QueryInfoPy: ...
def get_interactive_query_status(
    address: str,
    query_id: str,
    public_server_cert: bytes,
) -> TaskStatusType: ...
def do_query(
    address: str,
    plan: bytes,
    settings: bytes,
    public_server_cert: bytes,
) -> str: ...
