"""make carbon auditors email unique

Revision ID: 2ba0a3a85e00
Revises: 0b464a1d6c9c
Create Date: 2023-07-24 13:53:03.909649+00:00

"""
from typing import Any

from alembic import op

# revision identifiers, used by Alembic.
revision = '2ba0a3a85e00'
down_revision = '0b464a1d6c9c'
branch_labels = None
depends_on = None


def upgrade(is_dev: bool, **kw: Any) -> None:
    with op.batch_alter_table('carbon_auditor') as batch_op:
        batch_op.create_unique_constraint(constraint_name='carbon_auditor_uq_email', columns=['email'])


def downgrade(is_dev: bool, **kw: Any) -> None:
    with op.batch_alter_table('carbon_auditor') as batch_op:
        batch_op.drop_constraint('carbon_auditor_uq_email')
