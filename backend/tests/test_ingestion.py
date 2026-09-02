"""Unit & Integration Tests for Ingestion, OCR & Layout Domain."""

import io
from typing import Any

import pytest

from app.core.exceptions import IngestionError, UnsupportedFileTypeError
from app.domains.ingestion.service import IngestionService


@pytest.mark.asyncio
async def test_process_plain_text_document() -> None:
    service = IngestionService()
    sample_text = "INVOICE #4471\nACME CORP\nTotal Amount Due: $14,250.00\nNet 30"

    dto = await service.process_file(
        filename="test_invoice.txt",
        content_type="text/plain",
        file_bytes=sample_text.encode("utf-8"),
    )

    assert dto.filename == "test_invoice.txt"
    assert dto.page_count == 1
    assert len(dto.layout_blocks) >= 3
    assert dto.layout_blocks[0].block_type == "header"
    assert dto.layout_blocks[0].confidence >= 0.90


@pytest.mark.asyncio
async def test_unsupported_file_type_raises() -> None:
    service = IngestionService()
    with pytest.raises(UnsupportedFileTypeError):
        await service.process_file(
            filename="malicious.exe",
            content_type="application/x-msdownload",
            file_bytes=b"dummy",
        )


def _add_helvetica_font(writer: Any, page: Any) -> None:
    from pypdf.generic import DictionaryObject, NameObject

    font = DictionaryObject()
    font.update(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        }
    )
    font_ref = writer._add_object(font)
    resources = DictionaryObject()
    resources[NameObject("/Font")] = DictionaryObject({NameObject("/F1"): font_ref})
    page[NameObject("/Resources")] = resources


@pytest.mark.asyncio
async def test_process_text_pdf_extracts_content() -> None:
    """pypdf should extract text from a text-based PDF."""
    pypdf = pytest.importorskip("pypdf")

    # Build a minimal single-page text PDF in memory
    writer = pypdf.PdfWriter()
    page = writer.add_blank_page(width=612, height=792)
    _add_helvetica_font(writer, page)

    # Add text annotation as a simple overlay (pypdf approach)
    from pypdf.generic import DecodedStreamObject, NameObject

    stream = DecodedStreamObject()
    stream.set_data(
        b"BT /F1 12 Tf 72 720 Td (INVOICE #TEST-001 Total: $999.00 Vendor: ACME) Tj ET"
    )
    stream_ref = writer._add_object(stream)
    page[NameObject("/Contents")] = stream_ref

    buf = io.BytesIO()
    writer.write(buf)
    pdf_bytes = buf.getvalue()

    service = IngestionService()
    dto = await service.process_file(
        filename="test_invoice.pdf",
        content_type="application/pdf",
        file_bytes=pdf_bytes,
    )

    assert dto.page_count == 1
    assert dto.filename == "test_invoice.pdf"
    assert "INVOICE #TEST-001" in dto.raw_ocr_text
    assert "ACME" in dto.raw_ocr_text


@pytest.mark.asyncio
async def test_process_multipage_pdf_returns_correct_page_count() -> None:
    """Real multi-page PDFs must return the correct page_count, not hardcoded 1."""
    pypdf = pytest.importorskip("pypdf")
    from pypdf.generic import DecodedStreamObject, NameObject

    writer = pypdf.PdfWriter()
    for i in range(3):
        page = writer.add_blank_page(width=612, height=792)
        _add_helvetica_font(writer, page)
        stream = DecodedStreamObject()
        stream.set_data(
            f"BT /F1 12 Tf 72 720 Td (Annual Financial Report 2026 Section {i+1} Operating Revenue) Tj ET".encode()
        )
        stream_ref = writer._add_object(stream)
        page[NameObject("/Contents")] = stream_ref

    buf = io.BytesIO()
    writer.write(buf)
    pdf_bytes = buf.getvalue()

    service = IngestionService()
    dto = await service.process_file(
        filename="multipage_report.pdf",
        content_type="application/pdf",
        file_bytes=pdf_bytes,
    )

    assert dto.page_count == 3
    assert "Annual Financial Report" in dto.raw_ocr_text


@pytest.mark.asyncio
async def test_corrupted_pdf_raises_ingestion_error() -> None:
    """Corrupted or unreadable PDF bytes should raise IngestionError, not succeed silently."""
    service = IngestionService()
    corrupted = b"%PDF-1.4 \x00\xff\xfe garbage that is not a valid pdf stream"

    with pytest.raises(IngestionError) as exc_info:
        await service.process_file(
            filename="corrupted.pdf",
            content_type="application/pdf",
            file_bytes=corrupted,
        )

    # The error message should be user-readable
    assert exc_info.value.message
    assert len(exc_info.value.message) > 10
