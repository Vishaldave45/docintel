## Pull Request Description
<!-- Provide a clear summary of the changes and motivation -->

### Domain Affected
- [ ] Ingestion (OCR / Layout CV)
- [ ] Classification (Scikit-Learn ML Pipeline)
- [ ] Extraction (LangGraph / Agentic LLM)
- [ ] Retrieval (Sentence Transformers / FAISS RAG)
- [ ] API & Core (FastAPI / SQLAlchemy / Observability)
- [ ] Frontend (React / Ledger Design System)
- [ ] Infrastructure & CI/CD

### Linked Issues
Closes #<!-- issue number -->

---

### Key Changes
- 

### Architectural Compliance
- [ ] Adheres to domain boundaries (ADR-001)
- [ ] Does not leak ORM models into API contracts (ADR-002)
- [ ] Model artifact versioning updated if ML weights changed (ADR-003)
- [ ] LangGraph state schema changes validated (ADR-004)
- [ ] Frontend strictly adheres to 5-tone ledger palette & typography (ADR-005)

---

### Test Evidence
<!-- Paste test execution summary or coverage delta -->
```
====================== 42 passed in 1.48s ======================
```

### Pre-Merge Checklist
- [ ] `ruff check .` and `black --check .` passed
- [ ] `mypy .` passed with 0 errors
- [ ] `npm run lint` and `npm run build` passed
- [ ] New unit and integration tests added
- [ ] Documentation / ADRs updated if necessary
