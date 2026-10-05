import httpx
from .base import ActionStatus, ExecutionRef, PatchProvider, ProviderActionState

class BigFixProvider(PatchProvider):
    """BigFix REST adapter.

    BigFix-specific XML and REST responses terminate here. The orchestrator consumes
    the vendor-neutral PatchProvider contract, allowing additional patch tools later.
    """
    def __init__(self, base_url:str, username:str, password:str, verify_tls:bool=True):
        self._client=httpx.AsyncClient(base_url=base_url.rstrip("/"),auth=(username,password),verify=verify_tls,timeout=httpx.Timeout(30.0))

    async def health(self)->bool:
        response=await self._client.get("/api/help")
        return response.is_success

    async def execute(self,payload:str)->ExecutionRef:
        response=await self._client.post("/api/actions",content=payload,headers={"Content-Type":"application/xml"})
        response.raise_for_status()
        return ExecutionRef(provider="bigfix",external_id=response.text.strip())

    async def status(self,external_id:str)->ActionStatus:
        response=await self._client.get(f"/api/action/{external_id}/status")
        response.raise_for_status()
        # TODO: normalize the real BigFix action-status XML fixture into endpoint results.
        # Until the parser is implemented, preserve safe UNKNOWN semantics rather than
        # incorrectly declaring success from an HTTP 200 response.
        return ActionStatus(external_id=external_id,state=ProviderActionState.UNKNOWN)

    async def cancel(self,external_id:str)->None:
        response=await self._client.delete(f"/api/action/{external_id}")
        response.raise_for_status()

    async def capabilities(self)->set[str]:
        return {"execute","action_status","reporting","cancel","relevance"}
