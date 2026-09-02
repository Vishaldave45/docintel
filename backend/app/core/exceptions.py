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


class UnsupportedFileTypeError(IngestionError):
    """Raised when uploaded file format is not supported."""


class ClassificationError(DocIntelError):
    """Raised when ML document classifier cannot categorize input."""


class ModelArtifactNotFoundError(ClassificationError):
    """Raised when serialized pipeline or index artifact is missing."""


class ExtractionError(DocIntelError):
    """Raised when LangGraph extraction fails or violates output schema."""


class SchemaValidationError(ExtractionError):
    """Raised when structured fields fail strict Pydantic type checks."""


class RetrievalError(DocIntelError):
    """Raised when FAISS index retrieval or embedding fails."""


class DocumentNotFoundError(DocIntelError):
    """Raised when requested document ID does not exist."""
