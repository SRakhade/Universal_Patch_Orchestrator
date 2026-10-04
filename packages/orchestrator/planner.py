from .models import Campaign, CampaignType


class PlanningError(ValueError):
    pass


def validate_campaign(campaign: Campaign) -> Campaign:
    names = [stage.name for stage in campaign.stages]
    if len(names) != len(set(names)):
        raise PlanningError("Stage names must be unique")

    known = set(names)
    for stage in campaign.stages:
        missing = set(stage.depends_on) - known
        if missing:
            raise PlanningError(f"Stage {stage.name!r} has unknown dependencies: {sorted(missing)}")

    if campaign.campaign_type == CampaignType.RING and len(campaign.stages) < 2:
        raise PlanningError("Ring campaigns require at least two rings/stages")

    if campaign.campaign_type == CampaignType.CLUSTER:
        for stage in campaign.stages:
            if stage.batch_size not in (None, 1):
                raise PlanningError("Cluster stages must execute one node at a time by default")

    return campaign
