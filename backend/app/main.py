"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import health


def create_application() -> FastAPI:
    """Application factory for FastAPI service."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Backend API service for the Satellite-Based Multi-Hazard Disaster "
            "Risk Prediction and Early Warning System."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS middleware for local frontend development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # Mount API routers
    app.include_router(health.router)

    return app


app = create_application()
