"""wipe db

Revision ID: 8bafffffffff
Revises: 8bafe821dfce
Create Date: 2026-09-12 13:48:12.153568
"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = '8bafffffffff'
down_revision: str | None = '8bafe821dfce'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # WIPE the database
    op.execute("""
        TRUNCATE chats CASCADE;
        TRUNCATE users CASCADE;
    """)


def downgrade() -> None:
    pass
