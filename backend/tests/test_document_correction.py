"""Unit Tests for Document API Endpoints and Field Corrections."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.v1.documents import DOCUMENTS_STORE
from app.main import app


@pytest.mark.asyncio
async def test_update_document_fields_correction_endpoint() -> None:
    DOCUMENTS_STORE["doc-test-patch"] = {
        "id": "doc-test-patch",
        "filename": "invoice_sample.pdf",
        "content_type": "application/pdf",
        "file_size_bytes": 1024,
        "page_count": 1,
        "document_type": "invoice",
        "classifier_confidence": 0.95,
        "raw_ocr_text": "Sample invoice text with 14250 amount",
        "layout_blocks": [],
        "extraction_status": "needs_review",
        "flag_reason": None,
        "extracted_fields": {"invoice_number": "INV-100", "total_amount": 100.0},
        "validation_errors": ["Subtotal mismatch"],
        "repair_attempts": 2,
        "created_at": "2026-09-01T22:00:00Z",
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.patch(
            "/api/v1/documents/doc-test-patch/fields",
            json={"fields": {"total_amount": 14250.0, "vendor_name": "Acme Corp"}},
        )

        assert res.status_code == 200
        data = res.json()
        assert data["extraction_status"] == "verified"
        assert data["extracted_fields"]["total_amount"] == 14250.0
        assert data["extracted_fields"]["vendor_name"] == "Acme Corp"
        assert data["extracted_fields"]["invoice_number"] == "INV-100"
        assert data["validation_errors"] == []


@pytest.mark.asyncio
async def test_update_document_fields_404_on_missing_doc() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.patch(
            "/api/v1/documents/non-existent-doc/fields",
            json={"fields": {"total_amount": 500.0}},
        )
        assert res.status_code == 404
