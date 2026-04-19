from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.config import settings
from app.routers import health, mapping
from app.services.matcher import init_matcher

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: charger les données
    logger.info("startup", message="Chargement des données NAF/ROME...")
    init_matcher(settings.data_naf_path, settings.data_rome_path, settings.data_matching_path)
    logger.info("startup_complete", message="API prête !")
    yield
    # Shutdown
    logger.info("shutdown", message="Arrêt de l'API")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
## API de correspondance NAF <-> ROME

Cette API permet de :
- **Lister** les codes NAF et ROME
- **Rechercher** par mots-clés
- **Obtenir les correspondances** entre codes NAF et ROME
    """,
    lifespan=lifespan,
)

# CORS - permet les appels depuis n'importe quelle origine (utile pour le dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrement des routes
app.include_router(health.router)
app.include_router(mapping.router)


@app.get("/", tags=["Root"])
async def root() -> dict:
    """Page d'accueil de l'API."""
    return {
        "message": f"Bienvenue sur l'{settings.app_name} v{settings.app_version}",
        "docs": "/docs",
        "health": "/health",
    }
