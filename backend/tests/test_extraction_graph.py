"""Unit Tests for LangGraph State Machine and Self-Correction Repair Loop."""

import pytest

from app.domains.extraction.llm import build_gemini_extraction_model
from app.domains.extraction.service import ExtractionService


def test_build_gemini_extraction_model_uses_google_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.domains.extraction.llm.settings.gemini_api_key", "test-key")

    model = build_gemini_extraction_model()

    assert model is not None
    assert getattr(model, "model", None) == "gemini-1.5-flash"
    assert str(getattr(model, "google_api_key", None)) == "**********"


@pytest.mark.asyncio
async def test_extraction_graph_invoice_flow() -> None:
    service = ExtractionService()
    invoice_text = "INVOICE #4471\nTotal Amount: $14,250.00\nPayment Terms: Net 30"

    result = await service.extract_document_fields(
        document_id="test-doc-1",
        document_type="invoice",
        raw_ocr_text=invoice_text,
        layout_blocks=[],
    )

    assert result.target_schema == "InvoiceExtraction"
    assert result.is_valid is True
    assert result.fields.get("invoice_number") == "INV-4471"
    assert result.fields.get("total_amount") == 14250.0
    assert len(result.execution_trace) >= 3


@pytest.mark.asyncio
async def test_extraction_graph_contract_flow() -> None:
    service = ExtractionService()
    contract_text = "MASTER SERVICES AGREEMENT. Governing Law: State of Delaware."

    result = await service.extract_document_fields(
        document_id="test-doc-2",
        document_type="contract",
        raw_ocr_text=contract_text,
        layout_blocks=[],
    )

    assert result.target_schema == "ContractExtraction"
    assert "governing_law" in result.fields
    assert len(result.fields.get("parties", [])) >= 2


@pytest.mark.asyncio
async def test_extraction_graph_flagged_on_empty_or_short_text() -> None:
    service = ExtractionService()
    short_text = "low ocr"

    result = await service.extract_document_fields(
        document_id="test-doc-flagged",
        document_type="invoice",
        raw_ocr_text=short_text,
        layout_blocks=[],
    )

    assert result.status == "flagged"
    assert result.flag_reason is not None
    assert "short or degraded" in result.flag_reason


@pytest.mark.asyncio
async def test_extraction_graph_receipt_flow() -> None:
    service = ExtractionService()
    receipt_text = "Target Store #1044\nDate: 2026-08-29\nItem Purchase $42.50\nTax: $3.40\nTotal Amount Due: $45.90\nPayment: Visa"

    result = await service.extract_document_fields(
        document_id="test-doc-receipt-1",
        document_type="receipt",
        raw_ocr_text=receipt_text,
        layout_blocks=[],
    )

    assert result.target_schema == "ReceiptExtraction"
    assert result.is_valid is True
    assert result.fields.get("merchant_name") == "Target Store #1044"
    assert result.fields.get("total_amount") == 45.90
    assert result.fields.get("tax_amount") == 3.40
    assert result.fields.get("subtotal") == 42.50
    assert len(result.execution_trace) >= 3
