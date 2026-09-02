"""Unit & Integration Tests for Ingestion, OCR & Layout Domain."""

import pytest

from app.core.exceptions import UnsupportedFileTypeError
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
