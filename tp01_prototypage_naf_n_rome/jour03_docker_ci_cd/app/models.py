from pydantic import BaseModel, Field
from typing import Optional


class RomeEntry(BaseModel):
    code_rome: str = Field(..., description="Code ROME (ex: M1805)")
    name: str = Field(..., description="Intitulé du métier")
    desc: str = Field(..., description="Description du métier")

    model_config = {"from_attributes": True}


class NafEntry(BaseModel):
    code_naf: str = Field(..., description="Code NAF (ex: 62.01Z)")
    name: str = Field(..., description="Intitulé de l'activité")
    desc: str = Field(..., description="Description de l'activité")

    model_config = {"from_attributes": True}


class MappingResult(BaseModel):
    code_naf: str
    code_rome: str
    name: str
    desc: str
    score: Optional[float] = Field(None, description="Score de similarité (0-1)")


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=200, description="Mots-clés de recherche")
    limit: int = Field(default=10, ge=1, le=50, description="Nombre maximum de résultats")
    search_type: Optional[str] = Field(default="keyword", description="Type de recherche: 'keyword' ou 'semantic'")


class SearchResponse(BaseModel):
    query: str
    results: list[MappingResult]
    total: int
    search_type: str


class HealthResponse(BaseModel):
    status: str
    version: str
    records_loaded: int
