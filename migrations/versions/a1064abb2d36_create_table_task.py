"""create_table_task

Revision ID: a1064abb2d36
Revises: 
Create Date: 2022-11-03 13:50:31.446114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1064abb2d36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('task',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('title', sa.String(50), nullable=False),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('priority', sa.Integer(), nullable=False, default=6),
                    sa.Column('is_complete', sa.Boolean(), nullable=False, default=False))


def downgrade() -> None:
    op.drop_table('task')
