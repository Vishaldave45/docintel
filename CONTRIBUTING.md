# Contributing to DocIntel

Thank you for contributing to DocIntel! We hold high standards for code quality, architectural boundaries, test coverage, and documentation.

## 1. Branching Strategy & Git Workflow

DocIntel follows a structured **Trunk-Based / Protected Feature Branching** workflow:

- `main`: Always deployable, strictly protected. No direct commits allowed. All changes land via Pull Requests with passing CI checks and approvals.
- `develop`: Optional integration branch for grouped release staging.
- Feature / Bugfix branches must follow our naming convention:
  - `feat/<domain>-<short-description>` (e.g. `feat/extraction-add-repair-node`, `feat/ingestion-easyocr-segmentation`)
  - `fix/<short-description>` (e.g. `fix/classifier-empty-token-handling`)
  - `docs/<short-description>` (e.g. `docs/adr-007-pgvector-migration`)
  - `chore/<short-description>` (e.g. `chore/upgrade-faiss-cpu`)

### Commit Conventions
We enforce **Conventional Commits**:
- `feat(extraction): add fallback repair node for missing tax totals`
- `fix(retrieval): correct chunk overlap calculation in sentence splitter`
- `test(classification): add edge-case test for single-word receipts`
- `docs(adr): document ADR-005 frontend ledger design decisions`

### Merge Strategy
- **Squash and Merge** into `main` to preserve a clean, linear git history.

---

## 2. Pull Request Requirements
Every PR must fill out the `.github/PULL_REQUEST_TEMPLATE.md` with:
1. **Summary of Changes**: What domain was touched and why.
2. **Architecture Impact**: Does this alter service interfaces or require a new ADR?
3. **Testing Evidence**: CLI output or screenshots of passing pytest / vitest suites.
4. **Pre-flight Checklist**: Linting, type checks (`mypy`, `tsc`), and documentation updates.

---

## 3. Local Development Setup

### Backend (Python 3.11+)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest
```

### Frontend (Node 20+ & Vite)
```bash
npm install
npm run dev
```

### Full Stack via Docker
```bash
docker-compose up --build
```

---

## 4. Coding Standards

- **Python**: Strict `mypy` typing, `ruff` formatting and linting, 0 bare `except:`, domain boundaries respected (no importing sibling domain internals).
- **TypeScript / React**: Strict types, no `any`, tailwind utility styling conforming to the 5-tone ledger palette (`#F7F5F0`, `#211F1C`, `#2B3A55`, `#B33A2E`, `#8A7B4F`).
- **Tests**: Minimum 85% test coverage on domain services.
