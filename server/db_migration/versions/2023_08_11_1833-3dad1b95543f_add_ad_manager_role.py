"""add ad manager role

Revision ID: 3dad1b95543f
Revises: 7a747fe99a36
Create Date: 2023-08-11 18:33:39.343745+00:00

"""
from typing import Any

from alembic import op

# revision identifiers, used by Alembic.
revision = '3dad1b95543f'
down_revision = '7a747fe99a36'
branch_labels = None
depends_on = None


def upgrade(is_dev: bool, **kw: Any) -> None:
    op.execute('''
    INSERT INTO role(name)
    VALUES ('Ad Manager')
    ''')


def downgrade(is_dev: bool, **kw: Any) -> None:
    op.execute("DELETE FROM user_role "
               "WHERE role_id IN "
               "(SELECT id FROM role WHERE name = 'Ad Manager')")
    op.execute('''
    DELETE FROM role WHERE name = 'Ad Manager'
    ''')
