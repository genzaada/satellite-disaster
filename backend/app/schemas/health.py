"""Health check schema module."""

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Pydantic model representing backend health status."""
    status: str = Field(..., description="Operational status flag, e.g. 'ok'")
    version: str = Field(..., description="Semantic version of backend service")
    environment: str = Field(..., description="Current running environment")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of the health check"
    )
