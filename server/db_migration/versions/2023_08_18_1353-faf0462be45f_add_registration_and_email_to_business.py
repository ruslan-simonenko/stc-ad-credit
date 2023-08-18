"""add registration and email to business

Revision ID: faf0462be45f
Revises: 7a5d21d69bc1
Create Date: 2023-08-18 13:53:52.545913+00:00

"""
from typing import Any

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'faf0462be45f'
down_revision = '7a5d21d69bc1'
branch_labels = None
depends_on = None


def upgrade(is_dev: bool, **kw: Any) -> None:
    with op.batch_alter_table('business') as batch_op:
        batch_op.add_column(sa.Column('registration_type', sa.VARCHAR(64), nullable=False))
        batch_op.add_column(sa.Column('registration_number', sa.VARCHAR(64), nullable=False))
        batch_op.add_column(sa.Column('email', sa.VARCHAR(2048), nullable=True))
        batch_op.create_unique_constraint('business_uq_registration', [
            'registration_type',
            'registration_number',
        ])


def downgrade(is_dev: bool, **kw: Any) -> None:
    with op.batch_alter_table('business') as batch_op:
        batch_op.drop_constraint('business_uq_registration', type_='unique')
        batch_op.drop_column('email')
        batch_op.drop_column('registration_number')
        batch_op.drop_column('registration_type')
