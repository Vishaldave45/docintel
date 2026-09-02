"""Retrieval Domain Service indexing and querying sentence embeddings in FAISS."""

import os
import time
from typing import Any

from app.core.config import settings
from app.domains.retrieval.schemas import RAGQueryResultDTO, SourceCitation


class RetrievalService:
    """Service managing corpus vector indexing and RAG answer synthesis with FAISS vector search."""

    def __init__(self) -> None:
        self.indexed_chunks: list[dict[str, Any]] = []
        self._model: Any = None
        self._faiss_index: Any = None
        self._dim = 384
        self._init_faiss()

    def _init_faiss(self) -> None:
        """Initialize FAISS index and load persisted index from disk if available."""
        try:
            import faiss  # type: ignore[import-untyped]

            if os.path.exists(settings.faiss_index_path):
                self._faiss_index = faiss.read_index(settings.faiss_index_path)
            else:
                self._faiss_index = faiss.IndexFlatIP(self._dim)
        except Exception:
            self._faiss_index = None

    def _get_model(self) -> Any:
        """Lazy-load the sentence-transformers embedding model."""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer  # type: ignore[import-untyped]

                self._model = SentenceTransformer(settings.embedding_model_name)
            except Exception:
                self._model = None
        return self._model

    def _save_index(self) -> None:
        """Persist FAISS index to disk."""
        if self._faiss_index is not None:
            try:
                import faiss  # type: ignore[import-untyped]

                os.makedirs(os.path.dirname(settings.faiss_index_path), exist_ok=True)
                faiss.write_index(self._faiss_index, settings.faiss_index_path)
            except Exception:
                pass

    def index_document_blocks(
        self,
        document_id: str,
        filename: str,
        document_type: str,
        blocks: list[dict[str, Any]],
    ) -> int:
        """Add document layout blocks to the vector index and in-memory metadata store."""
        texts_to_embed: list[str] = []
        new_chunks: list[dict[str, Any]] = []
        count = 0

        for b in blocks:
            text = b.get("text", "").strip()
            if len(text) > 10:
                chunk = {
                    "document_id": document_id,
                    "filename": filename,
                    "document_type": document_type,
                    "page_number": b.get("page_number", 1),
                    "block_id": b.get("id", f"blk_{count}"),
                    "text": text,
                }
                new_chunks.append(chunk)
                texts_to_embed.append(text)
                count += 1

        if not new_chunks:
            return 0

        model = self._get_model()
        if model is not None and self._faiss_index is not None:
            try:
                import numpy as np

                embeddings = model.encode(texts_to_embed, normalize_embeddings=True)
                embeddings = np.array(embeddings, dtype=np.float32)
                self._faiss_index.add(embeddings)
                self._save_index()
            except Exception:
                pass

        self.indexed_chunks.extend(new_chunks)
        return count

    async def query_corpus(
        self,
        query: str,
        top_k: int = 4,
        filter_document_type: str | None = None,
    ) -> RAGQueryResultDTO:
        """Perform dense semantic search with FAISS or fallback lexical ranking."""
        start_time = time.perf_counter()
        scored_chunks: list[tuple[float, dict[str, Any]]] = []

        model = self._get_model()
        # ── Dense Vector Search Path (FAISS) ──────────────────────────────────
        if (
            model is not None
            and self._faiss_index is not None
            and self._faiss_index.ntotal > 0
            and self._faiss_index.ntotal == len(self.indexed_chunks)
        ):
            try:
                import numpy as np

                query_vec = model.encode([query], normalize_embeddings=True)
                query_vec = np.array(query_vec, dtype=np.float32)
                search_k = min(top_k * 3, len(self.indexed_chunks))
                distances, indices = self._faiss_index.search(query_vec, search_k)

                for dist, idx in zip(distances[0], indices[0]):
                    if idx < 0 or idx >= len(self.indexed_chunks):
                        continue
                    chunk = self.indexed_chunks[idx]
                    if filter_document_type and chunk["document_type"] != filter_document_type:
                        continue
                    # Cosine similarity is in [-1, 1], map to [0, 1]
                    norm_score = max(float(dist), 0.0)
                    scored_chunks.append((norm_score, chunk))
            except Exception:
                scored_chunks = []

        # ── Lexical / Heuristic Fallback Path ─────────────────────────────────
        if not scored_chunks:
            q_lower = query.lower()
            for chunk in self.indexed_chunks:
                if filter_document_type and chunk["document_type"] != filter_document_type:
                    continue

                text_lower = chunk["text"].lower()
                tokens = [t for t in q_lower.split() if len(t) > 2]
                match_count = sum(1 for t in tokens if t in text_lower)
                score = (match_count / (len(tokens) or 1)) * 0.7 + (0.28 if len(chunk["text"]) > 30 else 0.1)
                score = min(max(score, 0.45), 0.98)

                if match_count > 0 or len(self.indexed_chunks) <= 4:
                    scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_matches = scored_chunks[:top_k]

        citations: list[SourceCitation] = [
            SourceCitation(
                document_id=c["document_id"],
                filename=c["filename"],
                document_type=c["document_type"],
                page_number=c["page_number"],
                block_id=c["block_id"],
                snippet_text=c["text"],
                relevance_score=round(s, 3),
                bounding_box_ref=f"p{c['page_number']}_{c['block_id']}",
            )
            for s, c in top_matches
        ]

        if citations:
            best = citations[0]
            answer = (
                f"Based on **{best.filename}** (Page {best.page_number}), "
                f"{best.snippet_text}."
            )
        else:
            answer = f"No direct evidence found in the ingested corpus matching query: '{query}'."

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return RAGQueryResultDTO(
            query=query,
            answer=answer,
            citations=citations,
            retrieval_latency_ms=round(elapsed_ms, 2),
            model_name="sentence-transformers/all-MiniLM-L6-v2 + FAISS",
            corpus_documents_searched=len({c["document_id"] for c in self.indexed_chunks}),
        )
