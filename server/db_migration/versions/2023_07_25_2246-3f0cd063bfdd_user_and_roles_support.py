"""user and roles support

Revision ID: 3f0cd063bfdd
Revises: 2ba0a3a85e00
Create Date: 2023-07-25 22:46:35.122055+00:00

"""
from typing import Any

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3f0cd063bfdd'
down_revision = '2ba0a3a85e00'
branch_labels = None
depends_on = None


def upgrade(is_dev: bool, **kw: Any) -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('email', sa.VARCHAR(256), nullable=False, unique=True),
        sa.Column('name', sa.VARCHAR(256)),
        sa.Column('avatar_url', sa.VARCHAR(2048)),
    )
    op.create_table(
        'role',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('name', sa.VARCHAR(256), nullable=False, unique=True),
    )
    op.create_table(
        'user_role',
        sa.Column('id', sa.INTEGER, primary_key=True),
        sa.Column('user_id', sa.INTEGER, sa.ForeignKey('user.id'), nullable=False),
        sa.Column('role_id', sa.INTEGER, sa.ForeignKey('role.id'), nullable=False),
    )
    pass


def downgrade(is_dev: bool, **kw: Any) -> None:
    op.drop_table('user_role')
    op.drop_table('role')
    op.drop_table('user')
    pass
