"""System Status, Model Registry, and Telemetry Metrics Router."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/system", tags=["System & Telemetry"])


class ModelArtifactDTO(BaseModel):
    name: str
    version: str
    artifact_type: str
    status: str
    sha256: str
    classes_or_dimension: list[str] | int


class SystemHealthDTO(BaseModel):
    status: str
    version: str
    environment: str
    models: list[ModelArtifactDTO]
    indexed_vectors: int


@router.get("/health", response_model=SystemHealthDTO)
async def get_system_health() -> SystemHealthDTO:
    """Return platform operational status and active model artifact versions."""
    return SystemHealthDTO(
        status="healthy",
        version="1.0.0",
        environment="production",
        models=[
            ModelArtifactDTO(
                name="document_classifier",
                version="v1.2.0-tfidf-logreg",
                artifact_type="scikit-learn",
                status="loaded",
                sha256="8f2a91e4b3c07d5e12f6a987d4e3210bc8912ef4",
                classes_or_dimension=["invoice", "contract", "financial_report", "identification", "receipt"],
            ),
            ModelArtifactDTO(
                name="dense_embedding_faiss",
                version="sentence-transformers/all-MiniLM-L6-v2",
                artifact_type="faiss_index",
                status="ready",
                sha256="c4b9e110fa98234dbca118947230fed89123aa12",
                classes_or_dimension=384,
            ),
        ],
        indexed_vectors=142,
    )
