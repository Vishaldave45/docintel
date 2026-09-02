"""initial document schema

Revision ID: 001_initial_document_schema
Revises:
Create Date: 2026-09-02 12:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001_initial_document_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("content_type", sa.String(100), nullable=False),
        sa.Column("file_size_bytes", sa.Integer(), nullable=False),
        sa.Column("page_count", sa.Integer(), server_default="1"),
        # Classification
        sa.Column("document_type", sa.String(50), server_default="unknown"),
        sa.Column("classifier_confidence", sa.Float(), server_default="0.0"),
        sa.Column("classification_model_version", sa.String(50), server_default="v1.0.0"),
        # Ingestion & OCR
        sa.Column("raw_ocr_text", sa.Text(), nullable=False),
        sa.Column("layout_blocks", sa.JSON(), server_default="[]"),
        # Extraction
        sa.Column("extraction_status", sa.String(50), server_default="pending"),
        sa.Column("extracted_fields", sa.JSON(), server_default="{}"),
        sa.Column("validation_errors", sa.JSON(), server_default="[]"),
        sa.Column("repair_attempts", sa.Integer(), server_default="0"),
        # Retrieval
        sa.Column("is_indexed_in_faiss", sa.Boolean(), server_default="false"),
        sa.Column("faiss_vector_count", sa.Integer(), server_default="0"),
        # Audit
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("documents")

