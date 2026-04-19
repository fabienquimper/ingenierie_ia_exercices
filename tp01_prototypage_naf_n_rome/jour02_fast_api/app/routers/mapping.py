from fastapi import APIRouter, HTTPException, Query
from app.models import MappingResult, SearchRequest, SearchResponse, RomeEntry, NafEntry
from app.services.matcher import get_matcher
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["Mapping NAF-ROME"])


@router.get("/rome", summary="Lister les codes ROME")
async def list_rome(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict:
    """Retourne la liste paginée des codes ROME."""
    matcher = get_matcher()
    entries = matcher.get_rome_entries(limit=limit, offset=offset)
    return {"data": entries, "limit": limit, "offset": offset, "total": matcher.get_rome_count()}


@router.get("/rome/{code_rome}", summary="Détail d'un code ROME")
async def get_rome(code_rome: str) -> dict:
    """Retourne le détail d'un code ROME et les NAF associés."""
    matcher = get_matcher()
    rome = matcher.get_rome_by_code(code_rome)
    if not rome:
        raise HTTPException(status_code=404, detail=f"Code ROME '{code_rome}' non trouvé")
    naf_suggestions = matcher.get_naf_for_rome(code_rome)
    return {"rome": rome, "naf_suggestions": naf_suggestions}


@router.get("/naf", summary="Lister les codes NAF")
async def list_naf(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict:
    """Retourne la liste paginée des codes NAF."""
    matcher = get_matcher()
    entries = matcher.get_naf_entries(limit=limit, offset=offset)
    return {"data": entries, "limit": limit, "offset": offset, "total": matcher.get_naf_count()}


@router.get("/matching", summary="Lister les correspondances NAF↔ROME")
async def list_matching(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict:
    """Retourne la liste paginée des correspondances NAF↔ROME."""
    matcher = get_matcher()
    entries = matcher.get_matching_entries(limit=limit, offset=offset)
    return {"data": entries, "limit": limit, "offset": offset, "total": matcher.get_matching_count()}


@router.get("/all", summary="Charger toutes les données (usage frontend SPA)")
async def get_all() -> dict:
    """Retourne l'intégralité des enregistrements des 3 sources.
    Utilisé par le frontend Vue.js pour charger toutes les données en une seule requête.
    """
    matcher = get_matcher()
    data = matcher.get_all_entries()
    return {"data": data, "total": len(data)}


@router.get("/naf/{code_naf:path}", summary="Détail d'un code NAF")
async def get_naf(code_naf: str) -> dict:
    """Retourne le détail d'un code NAF et les ROME associés."""
    matcher = get_matcher()
    naf = matcher.get_naf_by_code(code_naf)
    if not naf:
        raise HTTPException(status_code=404, detail=f"Code NAF '{code_naf}' non trouvé")
    rome_suggestions = matcher.get_rome_for_naf(code_naf)
    return {"naf": naf, "rome_suggestions": rome_suggestions}


@router.post("/search", response_model=SearchResponse, summary="Recherche par mots-clés")
async def search(request: SearchRequest) -> SearchResponse:
    """Recherche des codes NAF/ROME par mots-clés."""
    matcher = get_matcher()
    raw_results = matcher.keyword_search(query=request.query, limit=request.limit)
    results = [
        MappingResult(
            code_naf=r.get("code_naf", ""),
            code_rome=r.get("code_rome", ""),
            name=r.get("name", ""),
            desc=r.get("desc", ""),
            score=float(r.get("score", 0)),
        )
        for r in raw_results
    ]
    return SearchResponse(
        query=request.query,
        results=results,
        total=len(results),
        search_type=request.search_type or "keyword",
    )


@router.get("/mapping/rome-to-naf/{code_rome}", summary="Correspondance ROME -> NAF")
async def mapping_rome_to_naf(code_rome: str) -> dict:
    """Retourne les codes NAF suggérés pour un code ROME donné."""
    matcher = get_matcher()
    results = matcher.get_naf_for_rome(code_rome)
    if not results:
        raise HTTPException(status_code=404, detail=f"Aucune correspondance NAF pour le code ROME '{code_rome}'")
    return {"code_rome": code_rome, "naf_suggestions": results}


@router.get("/mapping/naf-to-rome/{code_naf:path}", summary="Correspondance NAF -> ROME")
async def mapping_naf_to_rome(code_naf: str) -> dict:
    """Retourne les codes ROME suggérés pour un code NAF donné."""
    matcher = get_matcher()
    results = matcher.get_rome_for_naf(code_naf)
    if not results:
        raise HTTPException(status_code=404, detail=f"Aucune correspondance ROME pour le code NAF '{code_naf}'")
    return {"code_naf": code_naf, "rome_suggestions": results}
