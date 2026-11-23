from datetime import datetime
from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/", summary="Health Check")
def health_check():
    """Returns the operational status, server timestamp, and runtime environment of NEXORA."""
    return {
        "status": "healthy",
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
