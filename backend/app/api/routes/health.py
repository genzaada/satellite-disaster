"""Health check route module."""

from fastapi import APIRouter, status
from app.config import settings
from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Service Health Check",
    description="Returns service status, version, and current environment."
)
def get_health() -> HealthResponse:
    """Retrieve operational health information."""
    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )
