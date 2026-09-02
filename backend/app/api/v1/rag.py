"""FastAPI Router for Corpus RAG Q&A with Citations."""

from fastapi import APIRouter, Depends
from app.domains.retrieval.service import RetrievalService
from app.domains.retrieval.schemas import RAGQueryRequest, RAGQueryResultDTO

router = APIRouter(prefix="/rag", tags=["Retrieval & RAG"])

_retrieval_service_instance = RetrievalService()


def get_retrieval_service() -> RetrievalService:
    return _retrieval_service_instance


@router.post("/query", response_model=RAGQueryResultDTO)
async def query_corpus(
    request: RAGQueryRequest,
    service: RetrievalService = Depends(get_retrieval_service),
) -> RAGQueryResultDTO:
    """Perform grounded semantic search over all ingested documents with page/block citations."""
    return await service.query_corpus(
        query=request.query,
        top_k=request.top_k,
        filter_document_type=request.filter_document_type,
    )
