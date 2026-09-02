"""Unit Tests for PostgreSQL / Async SQLAlchemy DocumentRepository Layer."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.models import Base
from app.db.repository import DocumentRepository


@pytest_asyncio.fixture
async def test_session() -> AsyncSession:
    pytest.importorskip("aiosqlite")
    # Use in-memory SQLite with async sqlite driver
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_repository_crud_lifecycle(test_session: AsyncSession) -> None:
    repo = DocumentRepository(test_session)

    # 1. Create
    doc_data = {
        "id": "doc-repo-001",
        "filename": "Vendor_MSA.pdf",
        "content_type": "application/pdf",
        "file_size_bytes": 45000,
        "page_count": 4,
        "document_type": "contract",
        "classifier_confidence": 0.96,
        "raw_ocr_text": "MASTER SERVICES AGREEMENT between Parties...",
        "layout_blocks": [{"id": "blk_1", "text": "MSA", "block_type": "header"}],
        "extraction_status": "completed",
        "flag_reason": None,
        "extracted_fields": {"governing_law": "Delaware"},
        "validation_errors": [],
        "repair_attempts": 0,
    }

    created = await repo.create(doc_data)
    assert created.id == "doc-repo-001"
    assert created.filename == "Vendor_MSA.pdf"
    assert created.page_count == 4

    # 2. Get by ID
    retrieved = await repo.get("doc-repo-001")
    assert retrieved is not None
    assert retrieved.document_type == "contract"
    assert retrieved.extracted_fields["governing_law"] == "Delaware"

    # 3. List all
    all_docs = await repo.list_all()
    assert len(all_docs) == 1
    assert all_docs[0].id == "doc-repo-001"

    # 4. Update fields
    updated = await repo.update_fields(
        "doc-repo-001",
        {"governing_law": "California", "liability_cap": "$1M"},
        status="verified",
    )
    assert updated is not None
    assert updated.extraction_status == "verified"
    assert updated.extracted_fields["governing_law"] == "California"
    assert updated.extracted_fields["liability_cap"] == "$1M"

    # 5. Update extraction
    re_extracted = await repo.update_extraction(
        document_id="doc-repo-001",
        status="repaired",
        flag_reason=None,
        extracted_fields={"governing_law": "California", "term_years": 2},
        validation_errors=[],
        repair_attempts=1,
    )
    assert re_extracted is not None
    assert re_extracted.extraction_status == "repaired"
    assert re_extracted.repair_attempts == 1
