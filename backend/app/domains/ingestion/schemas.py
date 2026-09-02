"""Ingestion Domain DTOs and Schemas."""

from typing import Literal

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x: float = Field(..., description="Top left X coordinate normalized or pixel")
    y: float = Field(..., description="Top left Y coordinate normalized or pixel")
    width: float = Field(..., description="Width")
    height: float = Field(..., description="Height")


class LayoutBlockDTO(BaseModel):
    id: str
    block_type: Literal[
        "header", "paragraph", "table", "key_value", "signature", "stamp", "barcode"
    ]
    text: str
    confidence: float
    bbox: BoundingBox
    page_number: int = 1
    reading_order: int = 0


class IngestedDocumentDTO(BaseModel):
    document_id: str
    filename: str
    content_type: str
    file_size_bytes: int
    page_count: int
    raw_ocr_text: str
    layout_blocks: list[LayoutBlockDTO]
