"""chat member moderation state

Revision ID: a1c2e3f4b5d6
Revises: 70b60a66531c
Create Date: 2026-08-17 12:00:00.000000
"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = 'a1c2e3f4b5d6'
down_revision: str | None = '70b60a66531c'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'chat_members',
        sa.Column('state', sa.String(length=16), nullable=False, server_default='active'),
    )
    op.add_column(
        'chat_members',
        sa.Column('muted_until', sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('chat_members', 'muted_until')
    op.drop_column('chat_members', 'state')
