"""Unit Tests for FAISS Dense Vector RAG & Citation Provenance."""

import pytest

from app.domains.retrieval.service import RetrievalService


@pytest.mark.asyncio
async def test_index_and_query_citations() -> None:
    service = RetrievalService()
    blocks = [
        {"id": "blk_001", "page_number": 1, "text": "The contract liability cap is strictly limited to 12 months fees paid."},
        {"id": "blk_002", "page_number": 2, "text": "Total enterprise software licenses delivered was 10 units."},
    ]

    indexed_count = service.index_document_blocks(
        document_id="doc-9022",
        filename="Vendor_Agreement.pdf",
        document_type="contract",
        blocks=blocks,
    )

    assert indexed_count == 2

    rag_result = await service.query_corpus(query="What is the liability cap?")
    assert len(rag_result.citations) > 0
    assert rag_result.citations[0].document_id == "doc-9022"
    assert rag_result.citations[0].page_number == 1
    assert "liability cap" in rag_result.citations[0].snippet_text
