from fastapi import FastAPI, HTTPException

from packages.orchestrator.models import Campaign, CampaignCreate
from packages.orchestrator.planner import PlanningError, validate_campaign

app = FastAPI(
    title="Universal Patch Orchestrator API",
    version="0.1.0",
    description="Vendor-neutral patch orchestration control plane.",
)

_campaigns: dict[str, Campaign] = {}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/campaigns", response_model=Campaign, status_code=201)
async def create_campaign(request: CampaignCreate) -> Campaign:
    campaign = Campaign(**request.model_dump())
    try:
        validate_campaign(campaign)
    except PlanningError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    _campaigns[str(campaign.id)] = campaign
    return campaign


@app.get("/api/v1/campaigns", response_model=list[Campaign])
async def list_campaigns() -> list[Campaign]:
    return list(_campaigns.values())
