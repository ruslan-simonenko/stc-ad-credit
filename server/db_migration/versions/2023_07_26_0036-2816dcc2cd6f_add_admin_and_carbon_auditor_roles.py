"""add admin and carbon auditor roles

Revision ID: 2816dcc2cd6f
Revises: 3f0cd063bfdd
Create Date: 2023-07-26 00:36:09.658477+00:00

"""
from typing import Any

from alembic import op
from sqlalchemy import MetaData, Table

# revision identifiers, used by Alembic.
revision = '2816dcc2cd6f'
down_revision = '3f0cd063bfdd'
branch_labels = None
depends_on = None


def upgrade(is_dev: bool, **kw: Any) -> None:
    meta = MetaData()
    meta.reflect(bind=op.get_bind(), only=('role',))
    op.bulk_insert(Table('role', meta),
                   [{'name': 'Admin', },
                    {'name': 'Carbon Auditor', }])


def downgrade(is_dev: bool, **kw: Any) -> None:
    meta = MetaData()
    meta.reflect(bind=op.get_bind(), only=('role',))
    op.execute("DELETE FROM user_role "
               "WHERE role_id IN "
               "(SELECT role.id FROM role WHERE role.name IN ('Admin', 'Carbon Auditor'))")
    op.execute("DELETE FROM role WHERE name IN ('Admin', 'Carbon Auditor')")
