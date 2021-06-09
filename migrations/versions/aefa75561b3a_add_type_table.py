"""add_type_table

Revision ID: aefa75561b3a
Revises: 1ed89bc09097
Create Date: 2021-06-07 03:20:52.806729

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import ENUM


# revision identifiers, used by Alembic.
revision = 'aefa75561b3a'
down_revision = '1ed89bc09097'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('info', 'type')

    op.create_table(
        'type',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('pid', sa.BigInteger(), nullable=False),
        sa.Column('type', ENUM('Grass', 'Poison', 'Fire'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('pid', 'type')
    )

    op.create_foreign_key(
        'FK_info_type',
        'type',
        'info',
        ['pid'],
        ['id']
    )


def downgrade():
    op.drop_constraint('FK_info_type', 'type', type_='foreignkey')
    op.add_column('info', sa.Column('type', ENUM('Grass', 'Poison', 'Fire'), nullable=False))
    op.drop_table('type')
