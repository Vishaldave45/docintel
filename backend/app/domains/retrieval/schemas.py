"""Retrieval Domain Schemas & DTOs for Corpus RAG with Source Citations."""

from pydantic import BaseModel, Field


class SourceCitation(BaseModel):
    document_id: str
    filename: str
    document_type: str
    page_number: int = 1
    block_id: str
    snippet_text: str
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    bounding_box_ref: str | None = None


class RAGQueryRequest(BaseModel):
    query: str = Field(..., min_length=2, description="Natural language search or question")
    top_k: int = Field(default=4, ge=1, le=20)
    filter_document_type: str | None = None


class RAGQueryResultDTO(BaseModel):
    query: str
    answer: str
    citations: list[SourceCitation]
    retrieval_latency_ms: float
    model_name: str
    corpus_documents_searched: int
