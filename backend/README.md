# DocIntel Backend

FastAPI + SQLAlchemy 2.0 async backend for the DocIntel document intelligence platform.

## Stack

- **FastAPI** — async REST API
- **SQLAlchemy 2.0 async** — ORM with asyncpg driver
- **Alembic** — database migrations
- **Scikit-Learn** — TF-IDF document classification
- **LangGraph** — agentic extraction state machine
- **FAISS + sentence-transformers** — semantic RAG retrieval
- **pypdf + pytesseract** — PDF and OCR ingestion

## Development

```bash
pip install -e ".[dev,test]"
uvicorn app.main:app --reload
```

## Tests

```bash
pytest --cov=app tests/
```

## Migrations

```bash
alembic upgrade head
alembic revision --autogenerate -m "description"
```
