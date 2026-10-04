import httpx

from .base import ExecutionRef, PatchProvider


class BigFixProvider(PatchProvider):
    """BigFix REST adapter.

    Orchestration code must depend on PatchProvider, never directly on this class.
    """

    def __init__(self, base_url: str, username: str, password: str, verify_tls: bool = True):
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            auth=(username, password),
            verify=verify_tls,
            timeout=httpx.Timeout(30.0),
        )

    async def health(self) -> bool:
        response = await self._client.get("/api/help")
        return response.is_success

    async def execute(self, payload: str) -> ExecutionRef:
        response = await self._client.post(
            "/api/actions",
            content=payload,
            headers={"Content-Type": "application/xml"},
        )
        response.raise_for_status()
        # BigFix response parsing will be implemented with the first real action fixture.
        return ExecutionRef(provider="bigfix", external_id=response.text.strip())

    async def status(self, external_id: str) -> dict:
        response = await self._client.get(f"/api/action/{external_id}/status")
        response.raise_for_status()
        return {"external_id": external_id, "raw": response.text}

    async def cancel(self, external_id: str) -> None:
        response = await self._client.delete(f"/api/action/{external_id}")
        response.raise_for_status()
