"""create carbon audit table

Revision ID: 7a747fe99a36
Revises: 48786ee7ab66
Create Date: 2023-08-03 11:07:06.852766+00:00

"""
from typing import Any

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7a747fe99a36'
down_revision = '48786ee7ab66'
branch_labels = None
depends_on = None


def upgrade(is_dev: bool, **kw: Any) -> None:
    op.create_table(
        'carbon_audit',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('business_id', sa.INTEGER, sa.ForeignKey('business.id'), nullable=False),
        sa.Column('score', sa.INTEGER, nullable=False),
        sa.Column('report_date', sa.DATE, nullable=False),
        sa.Column('report_url', sa.VARCHAR(2048), nullable=False),
        sa.Column('created_by', sa.INTEGER, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('created_at', sa.DATETIME(timezone=True), nullable=False),
    )


def downgrade(is_dev: bool, **kw: Any) -> None:
    op.drop_table('carbon_audit')
