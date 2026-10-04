from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from packages.db.base import get_session
from packages.db.models import CampaignRecord
from packages.orchestrator.models import Campaign, CampaignCreate
from packages.orchestrator.planner import PlanningError, validate_campaign

app = FastAPI(title="Universal Patch Orchestrator API", version="0.2.0")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/v1/campaigns", response_model=Campaign, status_code=201)
async def create_campaign(request: CampaignCreate, session: AsyncSession = Depends(get_session)):
    campaign = Campaign(**request.model_dump())
    try:
        validate_campaign(campaign)
    except PlanningError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    record = CampaignRecord(
        id=campaign.id, name=campaign.name, campaign_type=campaign.campaign_type.value,
        provider=campaign.provider, status=campaign.status.value,
        definition=campaign.model_dump(mode="json"),
    )
    session.add(record)
    await session.commit()
    return campaign

@app.get("/api/v1/campaigns", response_model=list[Campaign])
async def list_campaigns(session: AsyncSession = Depends(get_session)):
    rows = (await session.execute(select(CampaignRecord).order_by(CampaignRecord.created_at.desc()))).scalars()
    return [Campaign.model_validate(row.definition) for row in rows]
