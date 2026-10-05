from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from packages.db.base import get_session
from packages.db.models import CampaignRecord, EndpointResultRecord, ProviderActionRecord
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

@app.get("/api/v1/reports/campaigns/{campaign_id}/summary")
async def campaign_report_summary(campaign_id: str, session: AsyncSession = Depends(get_session)):
    """Provider-neutral campaign execution summary used by the reporting UI."""
    counts = (await session.execute(
        select(EndpointResultRecord.state, func.count(EndpointResultRecord.id))
        .where(EndpointResultRecord.campaign_id == campaign_id)
        .group_by(EndpointResultRecord.state)
    )).all()
    by_state = {state: count for state, count in counts}
    total = sum(by_state.values())
    reboot_pending = await session.scalar(
        select(func.count(EndpointResultRecord.id)).where(
            EndpointResultRecord.campaign_id == campaign_id,
            EndpointResultRecord.reboot_required.is_(True),
        )
    )
    actions = (await session.execute(
        select(ProviderActionRecord).where(ProviderActionRecord.campaign_id == campaign_id)
        .order_by(ProviderActionRecord.created_at.desc())
    )).scalars().all()
    return {
        "campaign_id": campaign_id,
        "total": total,
        "successful": by_state.get("succeeded", 0),
        "failed": by_state.get("failed", 0),
        "running": by_state.get("running", 0),
        "pending": by_state.get("pending", 0),
        "unknown": by_state.get("unknown", 0),
        "reboot_pending": reboot_pending or 0,
        "provider_actions": [
            {"provider": a.provider, "external_id": a.external_id, "state": a.state}
            for a in actions
        ],
    }

@app.get("/api/v1/reports/campaigns/{campaign_id}/endpoints")
async def campaign_endpoint_report(campaign_id: str, session: AsyncSession = Depends(get_session)):
    rows = (await session.execute(
        select(EndpointResultRecord)
        .where(EndpointResultRecord.campaign_id == campaign_id)
        .order_by(EndpointResultRecord.endpoint_name)
    )).scalars().all()
    return [{
        "endpoint_id": r.endpoint_id, "endpoint_name": r.endpoint_name,
        "role": r.server_role, "os": r.os, "state": r.state,
        "exit_code": r.exit_code, "reboot_required": r.reboot_required,
        "failure_reason": r.failure_reason, "observed_at": r.observed_at,
    } for r in rows]
