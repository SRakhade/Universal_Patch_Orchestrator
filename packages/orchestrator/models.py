from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CampaignType(StrEnum):
    STANDARD = "standard"
    ROLLING = "rolling"
    RING = "ring"
    TIERED = "tiered"
    CLUSTER = "cluster"
    HYBRID = "hybrid"


class CampaignStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"


class Stage(BaseModel):
    name: str
    target_selector: str
    strategy: str = "all"
    batch_size: int | None = Field(default=None, ge=1)
    success_threshold: float = Field(default=100, ge=0, le=100)
    requires_approval: bool = False
    depends_on: list[str] = Field(default_factory=list)


class CampaignCreate(BaseModel):
    name: str = Field(min_length=3, max_length=120)
    campaign_type: CampaignType
    provider: str = "bigfix"
    stages: list[Stage] = Field(min_length=1)


class Campaign(CampaignCreate):
    id: UUID = Field(default_factory=uuid4)
    status: CampaignStatus = CampaignStatus.DRAFT
