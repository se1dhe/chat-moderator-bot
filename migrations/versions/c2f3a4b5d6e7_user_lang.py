"""add lang to user

Revision ID: c2f3a4b5d6e7
Revises: 8bafffffffff
Create Date: 2026-09-12 14:00:00.000000
"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = 'c2f3a4b5d6e7'
down_revision: str | None = '8bafffffffff'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('users', sa.Column('lang', sa.String(length=8), server_default='en', nullable=False))


def downgrade() -> None:
    op.drop_column('users', 'lang')
