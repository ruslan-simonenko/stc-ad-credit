"""add ad records table

Revision ID: 334449f20f01
Revises: 3dad1b95543f
Create Date: 2023-08-11 19:40:08.309948+00:00

"""
from typing import Any

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '334449f20f01'
down_revision = '3dad1b95543f'
branch_labels = None
depends_on = None


def upgrade(is_dev: bool, **kw: Any) -> None:
    op.create_table(
        'ad_record',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('business_id', sa.INTEGER, sa.ForeignKey('business.id'), nullable=False),
        sa.Column('ad_post_url', sa.VARCHAR(2048), nullable=False),
        sa.Column('created_by', sa.INTEGER, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('created_at', sa.DATETIME(timezone=True), nullable=False),
    )


def downgrade(is_dev: bool, **kw: Any) -> None:
    op.drop_table('ad_record')
