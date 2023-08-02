"""create business table

Revision ID: 48786ee7ab66
Revises: 2816dcc2cd6f
Create Date: 2023-08-02 13:38:49.266518+00:00

"""
from typing import Any

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '48786ee7ab66'
down_revision = '2816dcc2cd6f'
branch_labels = None
depends_on = None


def upgrade(is_dev: bool, **kw: Any) -> None:
    op.create_table(
        'business',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('name', sa.VARCHAR(256), nullable=False, unique=True),
        sa.Column('facebook_url', sa.VARCHAR(2048), nullable=True),
        sa.Column('created_by', sa.INTEGER, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('created_at', sa.DATETIME(timezone=True), nullable=False)
    )


def downgrade(is_dev: bool, **kw: Any) -> None:
    op.drop_table('business')
