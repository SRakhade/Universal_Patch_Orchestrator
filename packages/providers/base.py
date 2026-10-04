from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ExecutionRef:
    provider: str
    external_id: str


class PatchProvider(ABC):
    @abstractmethod
    async def health(self) -> bool: ...

    @abstractmethod
    async def execute(self, payload: str) -> ExecutionRef: ...

    @abstractmethod
    async def status(self, external_id: str) -> dict: ...

    @abstractmethod
    async def cancel(self, external_id: str) -> None: ...
