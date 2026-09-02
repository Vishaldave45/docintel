# DocIntel Development Setup Guide

This guide walks you through setting up DocIntel for local development on Linux (Ubuntu/Debian).

## System Requirements

Ensure you have the following installed:

- **Python 3.11+** (tested with 3.12.3)
- **Node.js 20+** (tested with v22.23.1)
- **npm 10+** (tested with 10.9.8)
- **Docker & Docker Compose** (for database and services)
- **PostgreSQL 15+** (via Docker)
- **Git**

Verify your setup:

```bash
python3 --version  # Should be >= 3.11
node --version     # Should be >= 20
npm --version      # Should be >= 10
docker --version   # Should be installed
```

---

## 1. Backend Setup (Python)

### 1.1 Create and Activate Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# On Windows: venv\Scripts\activate
```

### 1.2 Upgrade pip and Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -e .
```

This installs all dependencies from `pyproject.toml`, including:
- **FastAPI** — Web framework
- **SQLAlchemy** — ORM with async support
- **Pydantic** — Data validation
- **PyTorch & Transformers** — ML/AI models
- **LangChain & LangGraph** — Agentic LLM workflows
- **FAISS** — Dense vector search
- **Sentence Transformers** — Embeddings
- **Scikit-Learn** — Classification models
- **Tesseract & pdf2image** — Document processing

### 1.3 Install Optional Dev Dependencies (for testing)

```bash
pip install -e ".[test,dev]"
```

---

## 2. Frontend Setup (React + Vite)

### 2.1 Install Dependencies

```bash
cd ..  # Back to project root
npm install
```

This installs:
- **React 19** — UI framework
- **Vite 6** — Build tool
- **Tailwind CSS 4** — Styling
- **Express.js** — Backend server (for SSR)
- **TypeScript 5.8** — Type safety

### 2.2 Build Configuration

The project uses:
- `vite.config.ts` — Frontend build config
- `tsconfig.json` — TypeScript configuration
- `tailwind.config.js` — Tailwind styling

---

## 3. Database Setup

### 3.1 Start PostgreSQL with Docker

The project includes a `docker-compose.yml` configured for local development:

```bash
docker-compose up -d
```

This starts:
- **PostgreSQL** on `localhost:5432`
- Database: `docintel_db`
- User: `docintel`
- Password: `docintel_secret_password`

Verify the database is running:

```bash
docker-compose ps
```

### 3.2 Run Database Migrations

```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

This creates all required tables from the SQLAlchemy models in `db/models.py`.

---

## 4. Environment Configuration

### 4.1 Create `.env` File (Backend)

Create `backend/.env`:

```bash
cd backend
cat > .env << 'EOF'
ENV=development
DEBUG=true
PORT=8000
HOST=0.0.0.0

# Database (pre-configured via docker-compose)
DATABASE_URL=postgresql+asyncpg://docintel:docintel_secret_password@localhost:5432/docintel_db

# AI/ML Keys (optional, add your keys)
OPENAI_API_KEY=sk_your_key_here
GEMINI_API_KEY=your_key_here

# Logging
LOG_LEVEL=INFO

# Model Artifacts
MODEL_ARTIFACT_PATH=ml/artifacts/classification
FAISS_INDEX_PATH=ml/artifacts/retrieval/corpus_faiss.index
EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
EOF
```

See `backend/app/core/config.py` for all available settings.

---

## 5. Development Workflow

### 5.1 Backend Development Server

In one terminal:

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The FastAPI backend will start on `http://localhost:8000`.

**API Docs**: `http://localhost:8000/docs` (Swagger UI)

### 5.2 Frontend Development Server

In another terminal:

```bash
cd .  # Project root
npm run dev
```

The Vite dev server will start (typically on `http://localhost:5173`).

### 5.3 Testing Backend

Run unit tests:

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

Run specific test:

```bash
pytest tests/test_ingestion.py -v
```

With coverage:

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### 5.4 Linting & Type Checking

Lint Python code:

```bash
cd backend
source venv/bin/activate
ruff check app/
```

Format Python code:

```bash
black app/ tests/
```

TypeScript type checking:

```bash
npm run lint  # Runs tsc --noEmit
```

---

## 6. Project Structure

```
docintel/
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── api/v1/              # API routes
│   │   │   ├── documents.py
│   │   │   ├── rag.py
│   │   │   ├── system.py
│   │   │   └── router.py
│   │   ├── core/                # Configuration & exceptions
│   │   │   ├── config.py        # Pydantic settings
│   │   │   ├── exceptions.py
│   │   │   └── logging.py
│   │   ├── db/                  # Database models & session
│   │   │   ├── models.py        # SQLAlchemy ORM models
│   │   │   └── session.py       # AsyncSession factory
│   │   └── domains/             # Business logic (Domain-driven design)
│   │       ├── ingestion/       # Document ingestion (CV + OCR)
│   │       ├── classification/  # Doc type classification (Scikit-Learn)
│   │       ├── extraction/      # Field extraction (LangGraph)
│   │       └── retrieval/       # RAG query engine (FAISS + embeddings)
│   ├── tests/                   # Unit & integration tests
│   ├── venv/                    # Virtual environment
│   ├── Dockerfile               # Container image
│   └── pyproject.toml           # Dependencies
│
├── src/                         # React frontend (TypeScript)
│   ├── App.tsx
│   ├── main.tsx
│   ├── types.ts
│   └── components/              # React components
│       ├── Header.tsx
│       ├── DocumentDetailDrawer.tsx
│       ├── IngestModal.tsx
│       ├── RepoExplorer.tsx
│       ├── RAGMarginalView.tsx
│       ├── SystemHealthBanner.tsx
│       └── IndexCard.tsx
│
├── ml/                          # ML training & artifacts
│   └── classification/          # Classification model training
│       └── train.py
│
├── docs/                        # Architecture docs
│   └── adr/                     # Architecture Decision Records
│
├── public/                      # Static assets
├── server.ts                    # Express server (SSR)
├── vite.config.ts               # Vite build config
├── tsconfig.json                # TypeScript config
├── package.json                 # npm dependencies
├── Dockerfile                   # Frontend container image
├── docker-compose.yml           # Local dev services
├── README.md                    # Project overview
└── DEVELOPMENT.md               # This file
```

---

## 7. Architecture Overview

**DocIntel** is modular and follows Domain-Driven Design:

```
┌─────────────────────────────────┐
│   1. INGESTION                  │  (OCR, layout detection)
│      domains/ingestion          │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│   2. CLASSIFICATION              │  (Scikit-Learn TF-IDF)
│      domains/classification     │
└──────────────┬──────────────────┘
               ├──────────────────────────────┐
               ▼                              ▼
    ┌─────────────────────┐      ┌─────────────────────┐
    │ 3. EXTRACTION       │      │ 4. RETRIEVAL        │
    │ LangGraph Agent     │      │ FAISS + Embeddings  │
    │ (Self-correcting)   │      │ (Dense vector RAG)  │
    └─────────────────────┘      └─────────────────────┘
               │                              │
               └──────────────┬───────────────┘
                              ▼
                    ┌─────────────────────┐
                    │ 5. ARCHIVAL UI      │
                    │ React + Tailwind    │
                    │ (Index card UX)     │
                    └─────────────────────┘
```

Key services:
- **`api/v1/documents.py`** — Document CRUD
- **`api/v1/rag.py`** — RAG query interface
- **`api/v1/system.py`** — System health & stats

---

## 8. Common Development Tasks

### 8.1 Add a New API Endpoint

1. Create a route in `backend/app/api/v1/`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session

router = APIRouter(prefix="/v1/documents", tags=["documents"])

@router.get("/")
async def list_documents(session: AsyncSession = Depends(get_session)):
    # Your logic here
    pass
```

2. Register in `backend/app/api/v1/router.py`:

```python
from . import documents
app.include_router(documents.router)
```

### 8.2 Add a React Component

1. Create in `src/components/MyComponent.tsx`:

```typescript
import React from 'react';

export const MyComponent: React.FC = () => {
  return <div>My Component</div>;
};
```

2. Import in `src/App.tsx`:

```typescript
import { MyComponent } from './components/MyComponent';
```

### 8.3 Run Database Migrations

Create a new migration:

```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "Add user table"
alembic upgrade head
```

---

## 9. Troubleshooting

### Backend won't start - Module not found

Ensure virtual environment is activated:

```bash
cd backend
source venv/bin/activate
python -c "import app"  # Should work without error
```

### PostgreSQL connection refused

Verify Docker container is running:

```bash
docker-compose ps
docker-compose logs postgres
```

Restart services:

```bash
docker-compose down
docker-compose up -d
```

### Frontend build errors

Clear cache and reinstall:

```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Large package downloads timing out

Increase pip timeout:

```bash
pip install --default-timeout=1000 -e .
```

### CUDA/torch issues

If you don't have CUDA, the `faiss-cpu` and CPU-optimized PyTorch will be used. If you want GPU support, install `torch` with CUDA:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 10. Docker Deployment

### Build and Run Everything

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Build Only Backend or Frontend

```bash
# Backend image
docker build -f backend/Dockerfile -t docintel-backend .

# Frontend image
docker build -f Dockerfile -t docintel-frontend .
```

---

## 11. Contributing Guidelines

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on:
- Code style
- Commit messages
- Pull request process
- Testing requirements

---

## 12. Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **React Docs**: https://react.dev/
- **SQLAlchemy Async**: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **FAISS**: https://github.com/facebookresearch/faiss
- **Tailwind CSS**: https://tailwindcss.com/

---

## Support

For issues, questions, or feature requests, please open an issue on GitHub or contact the maintainers.

Happy developing! 🚀
