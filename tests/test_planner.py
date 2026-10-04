import pytest

from packages.orchestrator.models import Campaign, CampaignType, Stage
from packages.orchestrator.planner import PlanningError, validate_campaign


def test_ring_requires_multiple_stages():
    campaign = Campaign(
        name="October security rings",
        campaign_type=CampaignType.RING,
        stages=[Stage(name="canary", target_selector="group:canary")],
    )
    with pytest.raises(PlanningError, match="at least two"):
        validate_campaign(campaign)


def test_tier_dependencies_are_validated():
    campaign = Campaign(
        name="ERP tier patching",
        campaign_type=CampaignType.TIERED,
        stages=[
            Stage(
                name="application",
                target_selector="app:erp",
                depends_on=["database"],
            )
        ],
    )
    with pytest.raises(PlanningError, match="unknown dependencies"):
        validate_campaign(campaign)
