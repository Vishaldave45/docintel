"""DocIntel Typed Exception Hierarchy."""

from typing import Any


class DocIntelError(Exception):
    """Base exception for all domain errors."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class IngestionError(DocIntelError):
    """Raised when file parsing, OCR, or layout segmentation fails."""
    pass


class UnsupportedFileTypeError(IngestionError):
    """Raised when uploaded file format is not supported."""
    pass


class ClassificationError(DocIntelError):
    """Raised when ML document classifier cannot categorize input."""
    pass


class ModelArtifactNotFoundError(ClassificationError):
    """Raised when serialized pipeline or index artifact is missing."""
    pass


class ExtractionError(DocIntelError):
    """Raised when LangGraph extraction fails or violates output schema."""
    pass


class SchemaValidationError(ExtractionError):
    """Raised when structured fields fail strict Pydantic type checks."""
    pass


class RetrievalError(DocIntelError):
    """Raised when FAISS index retrieval or embedding fails."""
    pass


class DocumentNotFoundError(DocIntelError):
    """Raised when requested document ID does not exist."""
    pass
