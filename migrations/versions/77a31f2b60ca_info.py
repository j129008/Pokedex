"""info

Revision ID: 77a31f2b60ca
Revises: 
Create Date: 2021-06-06 13:53:19.767156

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import ENUM


# revision identifiers, used by Alembic.
revision = '77a31f2b60ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'evolution',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('before', sa.BigInteger(), nullable=False),
        sa.Column('after', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'info',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('name', sa.Integer(), nullable=False),
        sa.Column('type', ENUM('Grass', 'Poison', 'Fire'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('evolution')
    op.drop_table('info')
