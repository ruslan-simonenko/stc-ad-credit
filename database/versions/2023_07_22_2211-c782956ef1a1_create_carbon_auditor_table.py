"""create carbon auditor table

Revision ID: c782956ef1a1
Revises: 
Create Date: 2023-07-22 22:11:20.694268+00:00

"""
from typing import Any

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c782956ef1a1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade(**kw: Any) -> None:
    op.create_table(
        'carbon_auditor',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('email', sa.VARCHAR(256)),
        sa.Column('name', sa.VARCHAR(256)),
        sa.Column('picture_url', sa.VARCHAR(2048))
    )


def downgrade(**kw: Any) -> None:
    op.drop_table('carbon_auditor')
