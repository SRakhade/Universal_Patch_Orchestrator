from enum import StrEnum
from pydantic import BaseModel, Field

class ServerRole(StrEnum):
    APP = "app"
    MIDDLEWARE = "middleware"
    DATABASE = "database"
    LOAD_BALANCER = "load_balancer"
    WEB = "web"
    CACHE = "cache"
    MESSAGE_QUEUE = "message_queue"
    OTHER = "other"

class ClassificationSource(StrEnum):
    CMDB = "cmdb"
    BIGFIX_PROPERTY = "bigfix_property"
    MANUAL = "manual"
    INSTALLED_SOFTWARE = "installed_software"
    SERVICE_DISCOVERY = "service_discovery"
    NAMING_RULE = "naming_rule"

class ClassificationEvidence(BaseModel):
    source: ClassificationSource
    value: str
    confidence: int = Field(ge=0, le=100)

class ServerClassification(BaseModel):
    hostname: str
    application: str | None = None
    environment: str | None = None
    role: ServerRole
    cluster: str | None = None
    cluster_role: str | None = None
    verified: bool = False
    evidence: list[ClassificationEvidence] = Field(default_factory=list)
