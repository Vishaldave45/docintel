# ADR-001: Domain-Driven Modular Service Boundaries

- **Status:** Accepted
- **Date:** 2026-09-01
- **Deciders:** DocIntel Platform Architecture Team

## Context & Problem Statement
DocIntel is a multimodal document intelligence platform combining Computer Vision (Layout + OCR), Classical ML (Document Classification), Agentic LLM orchestration (Structured Extraction with LangGraph), and Vector Search (Corpus RAG with FAISS). If implemented as an intertwined monolithic module, cross-coupling between CV libraries, ML artifact loaders, LLM prompt templates, and vector store lifecycles quickly creates unmaintainable spaghetti code, testing friction, and dependency conflicts.

## Decision Drivers
- **Loose Coupling:** Ingestion (OCR/CV), Classification (Scikit-Learn), Extraction (LangGraph/LLM), and Retrieval (Embeddings/FAISS) evolve on different release cycles.
- **Independent Testability:** Ability to unit-test Scikit-Learn pipelines or FAISS indices in isolation with mock tensors/vectors without initializing LLM clients or PDF layout models.
- **Maintainable Layering:** Strict unidirectional dependency flow: `API Routers -> Domain Services -> Repositories/Engines -> Storage/Registry`.
- **Extensibility:** Easy swapping of OCR engines (e.g., Tesseract vs. EasyOCR vs. TrOCR) or Vector Indices (FAISS vs. pgvector vs. Qdrant) without touching extraction agents.

## Considered Options
1. **Single Monolithic Domain:** Single `backend/app/services/document_service.py` handling all tasks.
2. **Microservices from Day 1:** 4 separate HTTP microservices deployed independently.
3. **Domain-Driven Modular Monolith (Selected):** Split into `backend/app/domains/{ingestion, classification, extraction, retrieval}`, where each domain exposes a clean typed service interface and public Pydantic DTOs. Inter-domain communication occurs only via explicit service interfaces.

## Decision Outcome
Chosen Option: **Domain-Driven Modular Monolith**.

### Domain Breakdown
1. `backend/app/domains/ingestion`:
   - Responsibilities: Multipart file ingestion, PDF page rasterization, layout block segmentation (headers, tables, paragraphs), and OCR text extraction.
   - Public Interface: `IngestionService.process_document(file_bytes, filename) -> IngestedDocumentDTO`.
2. `backend/app/domains/classification`:
   - Responsibilities: Preprocessing, TF-IDF vectorization, multiclass ML classification (LogisticRegression/SVM), confidence scoring, feature contribution analysis.
   - Public Interface: `ClassificationService.classify_document(text, metadata) -> ClassificationResultDTO`.
3. `backend/app/domains/extraction`:
   - Responsibilities: LangGraph state machine orchestration, schema selection based on doc type, schema-constrained LLM extraction, validation loops, and self-correction/repair nodes.
   - Public Interface: `ExtractionService.extract_fields(document_type, ocr_text, layout_blocks) -> ExtractionResultDTO`.
4. `backend/app/domains/retrieval`:
   - Responsibilities: Text chunking, sentence transformer embeddings, FAISS vector index maintenance, similarity retrieval with hybrid BM25 + dense scoring, source citation mapping.
   - Public Interface: `RetrievalService.query_corpus(query, top_k, filter) -> RAGQueryResultDTO`.

## Consequences
- **Positive:** Pristine separation of concerns, no circular imports, clear ownership, easy transition to isolated microservices or serverless workers if workload scaling demands it.
- **Negative:** Requires strict discipline to avoid cross-domain internal imports. Enforced via `ruff` and `import-linter` rules in CI.
