"""add anonymize_events

Revision ID: 1cdeda440995
Revises: c2f3a4b5d6e7
Create Date: 2026-09-12 17:53:47.537630
"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = '1cdeda440995'
down_revision: str | None = 'c2f3a4b5d6e7'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("chat_settings", sa.Column("anonymize_events", sa.Boolean(), server_default=sa.text("false"), nullable=False))


def downgrade() -> None:
    op.drop_column("chat_settings", "anonymize_events")
