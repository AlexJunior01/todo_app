"""creating project table

Revision ID: cc9ab37bcb49
Revises: a1064abb2d36
Create Date: 2022-11-11 15:22:13.522751

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cc9ab37bcb49'
down_revision = 'a1064abb2d36'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'project',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(50), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('finished', sa.Boolean(), nullable=False, default=False)
    )

    op.add_column('task', sa.Column('project_id', sa.Integer, sa.ForeignKey('project.id')))


def downgrade() -> None:
    op.drop_column('task', 'project_id')
    op.drop_table('project')
