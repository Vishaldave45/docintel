"""Database Repository for Document CRUD operations using SQLAlchemy 2.0 Async."""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DocumentORM


class DocumentRepository:
    """Async repository encapsulating database queries for documents."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, doc_data: dict[str, Any]) -> DocumentORM:
        """Create and persist a new DocumentORM entity."""
        document = DocumentORM(**doc_data)
        self.session.add(document)
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def get(self, document_id: str) -> DocumentORM | None:
        """Retrieve a single document by its unique ID."""
        stmt = select(DocumentORM).where(DocumentORM.id == document_id)
        result = await self.session.execute(stmt)
        doc: DocumentORM | None = result.scalar_one_or_none()
        return doc

    async def list_all(self) -> Sequence[DocumentORM]:
        """Retrieve all documents ordered by creation time descending."""
        stmt = select(DocumentORM).order_by(DocumentORM.created_at.desc())
        result = await self.session.execute(stmt)
        docs: Sequence[DocumentORM] = result.scalars().all()
        return docs

    async def update_fields(
        self,
        document_id: str,
        fields: dict[str, Any],
        status: str = "verified",
    ) -> DocumentORM | None:
        """Update extracted fields and mark status as verified."""
        doc = await self.get(document_id)
        if not doc:
            return None

        current = dict(doc.extracted_fields or {})
        current.update(fields)
        doc.extracted_fields = current
        doc.extraction_status = status
        doc.validation_errors = []

        await self.session.commit()
        await self.session.refresh(doc)
        return doc

    async def update_extraction(
        self,
        document_id: str,
        status: str,
        flag_reason: str | None,
        extracted_fields: dict[str, Any],
        validation_errors: list[str],
        repair_attempts: int,
    ) -> DocumentORM | None:
        """Update extraction output from re-extract workflow."""
        doc = await self.get(document_id)
        if not doc:
            return None

        doc.extraction_status = status
        doc.flag_reason = flag_reason
        doc.extracted_fields = extracted_fields
        doc.validation_errors = validation_errors
        doc.repair_attempts = repair_attempts

        await self.session.commit()
        await self.session.refresh(doc)
        return doc
