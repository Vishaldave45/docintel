"""Unit Tests for LangGraph State Machine and Self-Correction Repair Loop."""

import pytest
from app.domains.extraction.service import ExtractionService


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
