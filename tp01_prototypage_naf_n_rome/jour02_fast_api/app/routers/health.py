from fastapi import APIRouter
from app.models import HealthResponse
from app.config import settings
from app.services.matcher import get_matcher

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Vérifie l'état de l'API et le nombre d'enregistrements chargés."""
    matcher = get_matcher()
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        records_loaded=matcher.record_count,
    )


@router.get("/metrics", tags=["Monitoring"])
async def metrics() -> dict:
    """Endpoint de métriques format simplifié."""
    matcher = get_matcher()
    return {
        "naf_rome_records_total": matcher.record_count,
        "api_status": 1,
    }
