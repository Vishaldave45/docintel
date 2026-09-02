# DocIntel — Multimodal Document Intelligence Platform

**DocIntel** is a modular, production-grade document intelligence platform that ingests unstructured physical paperwork (PDFs, scanned images) and transforms them into verified, queryable enterprise knowledge assets.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   DOCINTEL ARCHITECTURE                                │
└────────────────────────────────────────────────────────────────────────────────────────┘

  [ Physical Documents / Scans / PDFs ]
                   │
                   ▼
  ┌─────────────────────────────────┐
  │ 1. INGESTION (CV & Layout)      │ ──► Heuristic/Model Layout Detection
  │    `domains/ingestion`          │ ──► Multi-block OCR & Bounding Boxes
  └────────────────┬────────────────┘
                   │
                   ▼
  ┌─────────────────────────────────┐
  │ 2. CLASSIFICATION (Classical ML)│ ──► Scikit-Learn Pipeline (TF-IDF + LogReg)
  │    `domains/classification`     │ ──► Model Artifact Registry (`v1.2.0`)
  └────────────────┬────────────────┘
                   │
                   ├──────────────────────────────────┐
                   ▼                                  ▼
  ┌─────────────────────────────────┐ ┌─────────────────────────────────┐
  │ 3. EXTRACTION (Agentic LLM)     │ │ 4. RETRIEVAL (Corpus RAG)       │
  │    `domains/extraction`         │ │    `domains/retrieval`          │
  │  ┌───────────────────────────┐  │ │  ┌───────────────────────────┐  │
  │  │ LangGraph State Machine   │  │ │  │ Sentence-Transformers     │  │
  │  │ Type-Conditioned Routing  │  │ │  │ FAISS Dense Vector Index  │  │
  │  │ Pydantic Validation Loops │  │ │  │ Page/Block Source Cites   │  │
  │  │ Self-Correction Repairs   │  │ │  └───────────────────────────┘  │
  │  └───────────────────────────┘  │ └────────────────┬────────────────┘
  └────────────────┬────────────────┘                  │
                   │                                   │
                   └─────────────────┬─────────────────┘
                                     ▼
  ┌─────────────────────────────────────────────────────────────────────┐
  │ 5. ARCHIVAL FILING SYSTEM & USER INTERFACE (React + Vite)           │
  │    - 5-Tone Ledger Palette (#F7F5F0, #211F1C, #2B3A55, #B33A2E, #8A7B4F)│
  │    - Index Card Metaphor (INV, CTR, REP, ID, REC tab notches)       │
  │    - Marginal Citation RAG Q&A (Source line annotations)            │
  └─────────────────────────────────────────────────────────────────────┘
```

---

## Key Capabilities

1. **Computer Vision Layout & OCR**: Segments documents into semantic blocks (`header`, `table`, `key_value`, `paragraph`, `signature`) with normalized bounding coordinates and reading order.
2. **Classical ML Classification Pipeline**: Versioned Scikit-Learn TF-IDF vectorizer + multiclass classifier with feature attribution and n-gram explainability.
3. **Agentic Schema-Constrained Extraction (LangGraph)**:
   - Dynamic schema selection conditioned on detected document type.
   - Pydantic V2 validation loops with typed error lists.
   - Self-correction repair agent that recalibrates arithmetic consistency without failing the pipeline.
4. **Dense Vector RAG with Source Lineage**: Sentence transformer embeddings indexed in FAISS with exact page and block-level citations.
5. **Physical Ledger & Index Card UI**: Tailored for operations, finance, and legal teams using physical filing metaphors, ledger rules, and archival stamps.

---

## Architectural Decision Records (ADRs)

Detailed architectural justifications are cataloged in `/docs/adr/`:
- **[ADR-001: Domain-Driven Modular Service Boundaries](docs/adr/ADR-001-service-boundaries.md)**
- **[ADR-002: Asynchronous Backend with FastAPI & SQLAlchemy 2.0](docs/adr/ADR-002-async-backend.md)**
- **[ADR-003: Model Artifact Versioning & Hot-Reload Registry](docs/adr/ADR-003-model-artifact-versioning.md)**
- **[ADR-004: LangGraph State Graph Design for Type-Conditioned Extraction](docs/adr/ADR-004-langgraph-state-design.md)**
- **[ADR-005: Frontend Architecture & Physical Ledger Design Metaphor](docs/adr/ADR-005-frontend-architecture.md)**
- **[ADR-006: Observability, Structured Logging, and Metrics](docs/adr/ADR-006-observability.md)**

---

## Quickstart

### Boot Stack with Docker Compose
```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- FastAPI OpenAPI Docs: `http://localhost:8000/docs`

### Local Development

#### Backend (Python 3.11+)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,test]"
pytest
uvicorn app.main:app --reload --port 8000
```

#### Frontend (Node 20+)
```bash
npm install
npm run dev
```

---

## Retraining ML Classifiers
```bash
python ml/classification/train.py
```
Exports `ml/artifacts/classification/v1.2.0/pipeline.joblib` and `metadata.json` with stratified cross-validation reports.
