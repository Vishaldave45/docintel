"""FastAPI Router for Document Ingestion, Classification, and Extraction."""

from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel

from app.domains.classification.service import ClassificationService
from app.domains.extraction.service import ExtractionService
from app.domains.ingestion.service import IngestionService

router = APIRouter(prefix="/documents", tags=["Documents"])

# In-memory document store for fast prototype / local testing
DOCUMENTS_STORE: dict[str, dict[str, Any]] = {}


class DocumentDetailDTO(BaseModel):
    id: str
    filename: str
    content_type: str
    file_size_bytes: int
    page_count: int
    document_type: str
    classifier_confidence: float
    raw_ocr_text: str
    layout_blocks: list[dict[str, Any]]
    extraction_status: str
    extracted_fields: dict[str, Any]
    validation_errors: list[str]
    repair_attempts: int
    created_at: str


@router.post("/upload", response_model=DocumentDetailDTO, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    ingestion_service: IngestionService = Depends(IngestionService),
    classification_service: ClassificationService = Depends(ClassificationService),
    extraction_service: ExtractionService = Depends(ExtractionService),
) -> DocumentDetailDTO:
    """Full vertical slice: Ingest -> OCR & Layout -> Classify (ML) -> Extract (LangGraph) -> Store."""
    file_bytes = await file.read()

    # 1. Layout & OCR
    ingested = await ingestion_service.process_file(
        filename=file.filename or "uploaded_document",
        content_type=file.content_type or "application/octet-stream",
        file_bytes=file_bytes,
    )

    # 2. ML Classification
    classification = await classification_service.classify_text(ingested.raw_ocr_text)

    # 3. Agentic Extraction
    blocks_dicts = [b.model_dump() for b in ingested.layout_blocks]
    extraction = await extraction_service.extract_document_fields(
        document_id=ingested.document_id,
        document_type=classification.predicted_type,
        raw_ocr_text=ingested.raw_ocr_text,
        layout_blocks=blocks_dicts,
    )

    doc_entry = {
        "id": ingested.document_id,
        "filename": ingested.filename,
        "content_type": ingested.content_type,
        "file_size_bytes": ingested.file_size_bytes,
        "page_count": ingested.page_count,
        "document_type": classification.predicted_type,
        "classifier_confidence": classification.confidence,
        "raw_ocr_text": ingested.raw_ocr_text,
        "layout_blocks": blocks_dicts,
        "extraction_status": extraction.status,
        "extracted_fields": extraction.fields,
        "validation_errors": extraction.validation_errors,
        "repair_attempts": extraction.repair_attempts,
        "created_at": "2026-09-01T22:00:00Z",
    }
    DOCUMENTS_STORE[ingested.document_id] = doc_entry

    return DocumentDetailDTO(**doc_entry)


@router.get("", response_model=list[DocumentDetailDTO])
async def list_documents() -> list[DocumentDetailDTO]:
    """Retrieve all ingested documents in the repository."""
    return [DocumentDetailDTO(**d) for d in DOCUMENTS_STORE.values()]


@router.get("/{document_id}", response_model=DocumentDetailDTO)
async def get_document(document_id: str) -> DocumentDetailDTO:
    """Get single document details with layout blocks, classification, and extractions."""
    if document_id not in DOCUMENTS_STORE:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")
    return DocumentDetailDTO(**DOCUMENTS_STORE[document_id])
