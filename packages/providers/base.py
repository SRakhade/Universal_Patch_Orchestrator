from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum

class ProviderActionState(StrEnum):
    PENDING="pending"
    RUNNING="running"
    SUCCEEDED="succeeded"
    PARTIAL="partial"
    FAILED="failed"
    CANCELLED="cancelled"
    UNKNOWN="unknown"

@dataclass(frozen=True)
class ExecutionRef:
    provider: str
    external_id: str

@dataclass(frozen=True)
class EndpointResult:
    endpoint_id: str
    endpoint_name: str
    state: str
    exit_code: int | None = None
    message: str | None = None
    reboot_required: bool | None = None

@dataclass(frozen=True)
class ActionStatus:
    external_id: str
    state: ProviderActionState
    total: int = 0
    succeeded: int = 0
    failed: int = 0
    pending: int = 0
    endpoints: tuple[EndpointResult,...] = ()

class PatchProvider(ABC):
    """Vendor-neutral contract implemented by every patch-management integration."""

    @abstractmethod
    async def health(self) -> bool: ...

    @abstractmethod
    async def execute(self, payload: str) -> ExecutionRef: ...

    @abstractmethod
    async def status(self, external_id: str) -> ActionStatus: ...

    @abstractmethod
    async def cancel(self, external_id: str) -> None: ...

    async def capabilities(self) -> set[str]:
        return {"execute","action_status","reporting"}
