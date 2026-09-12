"""cloud ai settings

Revision ID: 9a9b8c7d6e5f
Revises: 17e49d664826
Create Date: 2026-09-11 20:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a9b8c7d6e5f'
down_revision = 'a1c2e3f4b5d6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('chat_settings', sa.Column('ai_provider', sa.String(length=16), server_default='ollama', nullable=False))
    op.add_column('chat_settings', sa.Column('ai_model', sa.String(length=64), nullable=True))
    op.add_column('chat_settings', sa.Column('ai_api_key_encrypted', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('chat_settings', 'ai_api_key_encrypted')
    op.drop_column('chat_settings', 'ai_model')
    op.drop_column('chat_settings', 'ai_provider')
