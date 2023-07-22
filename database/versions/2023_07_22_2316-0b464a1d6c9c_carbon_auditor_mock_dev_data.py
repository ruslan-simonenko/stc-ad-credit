"""carbon auditor - mock dev data

Revision ID: 0b464a1d6c9c
Revises: c782956ef1a1
Create Date: 2023-07-22 23:16:19.151162+00:00

"""
from typing import Any

from alembic import op
import sqlalchemy as sa
from sqlalchemy import MetaData, Table

# revision identifiers, used by Alembic.
revision = '0b464a1d6c9c'
down_revision = 'c782956ef1a1'
branch_labels = None
depends_on = None


def upgrade(is_dev: bool, **kw: Any) -> None:
    if not is_dev:
        return
    meta = MetaData()
    meta.reflect(bind=op.get_bind(), only=('carbon_auditor',))
    op.bulk_insert(Table('carbon_auditor', meta),
                   [{
                       'email': 'jane.doe@gmail.com',
                       'name': 'Jane Doe',
                       'picture_url': 'https://cdn.quasar.dev/img/avatar2.jpg',
                   }, {
                       'email': 'john.doe@gmail.com',
                       'name': 'John Doe',
                       'picture_url': 'https://cdn.quasar.dev/img/avatar4.jpg',
                   }])


def downgrade(is_dev: bool, **kw: Any) -> None:
    if not is_dev:
        return
    op.execute('DELETE FROM carbon_auditor;')
