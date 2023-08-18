"""add business manager

Revision ID: 7a5d21d69bc1
Revises: 334449f20f01
Create Date: 2023-08-18 11:26:15.667556+00:00

"""
from typing import Any

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7a5d21d69bc1'
down_revision = '334449f20f01'
branch_labels = None
depends_on = None


def upgrade(is_dev: bool, **kw: Any) -> None:
    op.execute('''
        INSERT INTO role(name)
        VALUES ('Business Manager')
        ''')


def downgrade(is_dev: bool, **kw: Any) -> None:
    op.execute("DELETE FROM user_role "
               "WHERE role_id IN "
               "(SELECT id FROM role WHERE name = 'Business Manager')")
    op.execute('''
       DELETE FROM role WHERE name = 'Business Manager'
       ''')
