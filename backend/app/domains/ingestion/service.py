"""Ingestion Service implementing layout segmentation and OCR."""

import uuid
from typing import ClassVar

from app.core.exceptions import IngestionError, UnsupportedFileTypeError
from app.domains.ingestion.schemas import BoundingBox, IngestedDocumentDTO, LayoutBlockDTO


class IngestionService:
    """Service handling document layout detection, bounding-box segmentation, and OCR."""

    SUPPORTED_TYPES: ClassVar[set[str]] = {
        "application/pdf", "image/png", "image/jpeg", "image/tiff", "text/plain"
    }

    # Minimum meaningful OCR text length; below this we flag the document.
    _MIN_TEXT_LENGTH: ClassVar[int] = 20

    async def process_file(
        self,
        filename: str,
        content_type: str,
        file_bytes: bytes,
    ) -> IngestedDocumentDTO:
        """Parse raw file bytes into OCR text and structured layout blocks."""
        if content_type not in self.SUPPORTED_TYPES and not filename.endswith(
            (".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".txt")
        ):
            raise UnsupportedFileTypeError(
                f"File type '{content_type}' is not supported. Allowed: PDF, PNG, JPG, TIFF, TXT."
            )

        doc_id = str(uuid.uuid4())

        # ── Plain text ──────────────────────────────────────────────────────────
        if content_type == "text/plain" or filename.endswith(".txt"):
            text = file_bytes.decode("utf-8", errors="replace")
            blocks = self._segment_text_to_layout(text)
            return IngestedDocumentDTO(
                document_id=doc_id,
                filename=filename,
                content_type=content_type,
                file_size_bytes=len(file_bytes),
                page_count=1,
                raw_ocr_text=text,
                layout_blocks=blocks,
            )

        # ── PDF ─────────────────────────────────────────────────────────────────
        if content_type == "application/pdf" or filename.lower().endswith(".pdf"):
            text, page_count, flag_reason = self._extract_pdf_text(file_bytes, filename)
            if flag_reason:
                raise IngestionError(flag_reason, details={"filename": filename, "flag_reason": flag_reason})
            blocks = self._segment_text_to_layout(text)
            return IngestedDocumentDTO(
                document_id=doc_id,
                filename=filename,
                content_type=content_type,
                file_size_bytes=len(file_bytes),
                page_count=page_count,
                raw_ocr_text=text,
                layout_blocks=blocks,
            )

        # ── Image (PNG / JPG / TIFF) ────────────────────────────────────────────
        text, flag_reason = self._extract_image_text(file_bytes, filename)
        if flag_reason:
            raise IngestionError(flag_reason, details={"filename": filename, "flag_reason": flag_reason})
        blocks = self._segment_text_to_layout(text)
        return IngestedDocumentDTO(
            document_id=doc_id,
            filename=filename,
            content_type=content_type,
            file_size_bytes=len(file_bytes),
            page_count=1,
            raw_ocr_text=text,
            layout_blocks=blocks,
        )

    # ── Private PDF extractor ────────────────────────────────────────────────────

    def _extract_pdf_text(
        self, file_bytes: bytes, filename: str
    ) -> tuple[str, int, str | None]:
        """Extract text from a PDF.

        Returns (text, page_count, flag_reason).
        flag_reason is None on success; a plain-language string on failure.

        Strategy:
          1. Try pypdf (fast, zero-dependency, works for text-based PDFs).
          2. Fall back to pdf2image + pytesseract for scanned/image PDFs.
          3. If both fail or yield < _MIN_TEXT_LENGTH chars, return a flag_reason.
        """
        import io

        # ── Attempt 1: pypdf ────────────────────────────────────────────────────
        try:
            import pypdf  # type: ignore[import-untyped]

            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            page_count = len(reader.pages)
            pages_text: list[str] = []
            for page in reader.pages:
                extracted = page.extract_text() or ""
                pages_text.append(extracted)
            full_text = "\n".join(pages_text).strip()

            if len(full_text) >= self._MIN_TEXT_LENGTH:
                return full_text, page_count, None
            # Text too short — try OCR fallback before flagging
        except Exception:  # pypdf can raise PdfReadError and others
            page_count = 1  # unknown until we try OCR

        # ── Attempt 2: pdf2image + pytesseract ─────────────────────────────────
        try:
            import pytesseract  # type: ignore[import-untyped]
            from pdf2image import convert_from_bytes  # type: ignore[import-untyped]

            images = convert_from_bytes(file_bytes, dpi=200)
            page_count = len(images)
            ocr_pages: list[str] = []
            for img in images:
                ocr_pages.append(pytesseract.image_to_string(img))
            full_text = "\n".join(ocr_pages).strip()

            if len(full_text) >= self._MIN_TEXT_LENGTH:
                return full_text, page_count, None

            # Both pypdf and OCR produced near-empty text
            return (
                full_text,
                page_count,
                (
                    f"Scan quality too low to extract readable text from '{filename}'. "
                    "Please re-upload a higher-resolution scan."
                ),
            )
        except Exception as exc:
            # If pypdf successfully read the structure/page count, return whatever text was found
            if page_count > 0:
                return (
                    full_text if 'full_text' in locals() else "",
                    page_count,
                    None if ('full_text' in locals() and len(full_text) >= self._MIN_TEXT_LENGTH)
                    else f"Scan quality too low or OCR unavailable for '{filename}'.",
                )
            return (
                "",
                1,
                (
                    f"Could not process '{filename}': {exc}. "
                    "Ensure the file is a valid, non-corrupted PDF."
                ),
            )

    # ── Private image extractor ─────────────────────────────────────────────────

    def _extract_image_text(
        self, file_bytes: bytes, filename: str
    ) -> tuple[str, str | None]:
        """OCR a single-page image file. Returns (text, flag_reason)."""
        try:
            import io

            import pytesseract  # type: ignore[import-untyped]
            from PIL import Image

            img = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(img).strip()

            if len(text) >= self._MIN_TEXT_LENGTH:
                return text, None

            return (
                text,
                (
                    f"Image '{filename}' produced insufficient text ({len(text)} characters). "
                    "Ensure the image is clear and contains readable text."
                ),
            )
        except Exception as exc:
            return (
                "",
                (
                    f"Failed to read image '{filename}': {exc}. "
                    "Supported formats: PNG, JPG, TIFF."
                ),
            )

    # ── Layout segmenter ────────────────────────────────────────────────────────

    def _segment_text_to_layout(self, text: str) -> list[LayoutBlockDTO]:
        """Heuristic rule-based layout analyzer identifying headers, tables, key-values, and paragraphs."""
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        blocks: list[LayoutBlockDTO] = []

        y_cursor = 40.0
        for idx, line in enumerate(lines):
            block_type = "paragraph"
            if idx == 0 or line.isupper() or (
                len(line) < 45
                and (
                    "INVOICE" in line.upper()
                    or "AGREEMENT" in line.upper()
                    or "REPORT" in line.upper()
                )
            ):
                block_type = "header"
            elif ":" in line and len(line.split(":")[0]) < 25:
                block_type = "key_value"
            elif "|" in line or "\t" in line or ("$" in line and any(c.isdigit() for c in line)):
                block_type = "table"

            blocks.append(
                LayoutBlockDTO(
                    id=f"blk_{idx+1:03d}",
                    block_type=block_type,  # type: ignore[arg-type]
                    text=line,
                    confidence=0.97 if block_type == "header" else 0.94,
                    bbox=BoundingBox(
                        x=40.0,
                        y=y_cursor,
                        width=520.0,
                        height=24.0 if block_type != "table" else 36.0,
                    ),
                    page_number=1,
                    reading_order=idx,
                )
            )
            y_cursor += 32.0

        return blocks
