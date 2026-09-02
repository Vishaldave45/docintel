"""add flag_reason column to documents

Revision ID: 002_add_flag_reason
Revises: 001_initial_document_schema
Create Date: 2026-09-02 12:35:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "002_add_flag_reason"
down_revision: str | None = "001_initial_document_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("flag_reason", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "flag_reason")
