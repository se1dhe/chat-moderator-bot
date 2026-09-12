"""grant pro to se1dhe

Revision ID: 8bafe821dfce
Revises: 9a9b8c7d6e5f
Create Date: 2026-09-12 13:00:12.153568
"""
from __future__ import annotations

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = '8bafe821dfce'
down_revision: str | None = '9a9b8c7d6e5f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Grant PRO subscription to any chat matching se1dhe.dev or se1dhe
    op.execute("""
        INSERT INTO subscriptions (chat_telegram_id, plan, created_at)
        SELECT telegram_id, 'pro', NOW()
        FROM chats
        WHERE title ILIKE '%se1dhe.dev%' OR username ILIKE '%se1dhe%'
        ON CONFLICT (chat_telegram_id) DO UPDATE SET plan = 'pro';
    """)


def downgrade() -> None:
    pass
