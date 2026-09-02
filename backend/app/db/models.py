"""SQLAlchemy 2.0 Async Models and Base."""

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarative class with common audit fields."""


class DocumentORM(Base):
    """Document entity storing ingestion metadata, classification, and extractions."""

    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    page_count: Mapped[int] = mapped_column(Integer, default=1)

    # Classification Results
    document_type: Mapped[str] = mapped_column(String(50), default="unknown")
    classifier_confidence: Mapped[float] = mapped_column(Float, default=0.0)
    classification_model_version: Mapped[str] = mapped_column(String(50), default="v1.0.0")

    # Ingestion & OCR
    raw_ocr_text: Mapped[str] = mapped_column(Text, nullable=False)
    layout_blocks: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)

    # Extraction State
    extraction_status: Mapped[str] = mapped_column(String(50), default="pending")  # pending | completed | needs_review | flagged | failed
    flag_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    extracted_fields: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    validation_errors: Mapped[list[str]] = mapped_column(JSON, default=list)
    repair_attempts: Mapped[int] = mapped_column(Integer, default=0)

    # Retrieval Indexing
    is_indexed_in_faiss: Mapped[bool] = mapped_column(Boolean, default=False)
    faiss_vector_count: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
