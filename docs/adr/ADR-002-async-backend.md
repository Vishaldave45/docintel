# ADR-002: Asynchronous Backend with FastAPI, SQLAlchemy 2.0 & PostgreSQL

- **Status:** Accepted
- **Date:** 2026-09-01
- **Deciders:** DocIntel Platform Architecture Team

## Context & Problem Statement
Document processing pipelines require handling high-latency operations (OCR inference, model matrix multiplications, LLM streaming calls, vector indexing) alongside high-concurrency metadata queries. A synchronous blocking architecture (such as Flask or Django WSGI) risks thread starvation during long LLM calls.

## Decision Drivers
- **Non-blocking I/O:** Concurrently serve document query requests while background worker tasks or streaming LLM responses execute.
- **Strict Layering:** Clear boundary between database entities (SQLAlchemy ORM) and API contracts (Pydantic V2).
- **Migration Safety:** Declarative, reversible schema migrations using Alembic.
- **Type Safety:** Full `asyncio` and `mypy` strict compliance with SQLAlchemy 2.0 typed mappings.

## Architecture Pattern
```
[HTTP Request]
     │
     ▼
[API Router (v1)] ──► Depends(get_db_session), Depends(get_service)
     │
     ▼
[Domain Service] ──► Business Logic, LangGraph, ML Inferences
     │
     ▼
[Repository Layer] ──► Async SQLAlchemy 2.0 queries
     │
     ▼
[PostgreSQL Database] (Asyncpg driver)
```

## Key Rules
1. **Never return ORM models from API routes**: Every endpoint converts ORM objects to validated Pydantic DTOs before responding.
2. **Session Lifecycles**: Sessions are injected using `async with get_async_session() as session:` with automatic commit/rollback semantics.
3. **Heavy CPU Isolation**: Long-running layout segmentation and embeddings generation are offloaded to thread/process pools (`run_in_executor`) to keep the FastAPI asyncio event loop unblocked.

## Consequences
- **Positive:** High throughput, low memory footprint, first-class async OpenAPI documentation, deterministic connection pooling.
- **Negative:** Async SQLAlchemy requires careful handling of eager/lazy relationship loading (`selectinload`).
