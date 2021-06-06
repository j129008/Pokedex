"""add_evolution_fk

Revision ID: 1ed89bc09097
Revises: 77a31f2b60ca
Create Date: 2021-06-06 14:22:30.824179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ed89bc09097'
down_revision = '77a31f2b60ca'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        'FK_evolution_before_id',
        'evolution',
        'info',
        ['before'],
        ['id']
    )

    op.create_foreign_key(
        'FK_evolution_after_id',
        'evolution',
        'info',
        ['after'],
        ['id']
    )


def downgrade():
    op.drop_constraint('FK_evolution_before_id', 'evolution', type_='foreignkey')
    op.drop_constraint('FK_evolution_after_id', 'evolution', type_='foreignkey')
