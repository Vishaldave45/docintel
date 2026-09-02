"""Unit Tests for Scikit-Learn Document Classification Pipeline."""

import pytest

from app.domains.classification.service import ClassificationService


@pytest.mark.asyncio
async def test_classify_invoice_tokens() -> None:
    service = ClassificationService()
    invoice_text = "INVOICE #9901 Bill To: Acme Corp Subtotal: $5,000 Tax: $500 Total Amount: $5,500 Remit Payment"

    result = await service.classify_text(invoice_text)
    assert result.predicted_type == "invoice"
    assert result.confidence >= 0.70
    assert len(result.top_features) > 0
    assert any("invoice" in f.feature_ngram for f in result.top_features)


@pytest.mark.asyncio
async def test_classify_contract_tokens() -> None:
    service = ClassificationService()
    contract_text = "MASTER SERVICES AGREEMENT between Parties. Indemnification, Governing Law Delaware, and Confidentiality."

    result = await service.classify_text(contract_text)
    assert result.predicted_type == "contract"
    assert result.confidence >= 0.70
