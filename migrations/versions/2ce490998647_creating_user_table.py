"""creating_user_table

Revision ID: 2ce490998647
Revises: cc9ab37bcb49
Create Date: 2022-12-24 17:56:33.882282

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2ce490998647'
down_revision = 'cc9ab37bcb49'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(), nullable=False, unique=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, default=True)
    )

    op.add_column('task', sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')))
    op.add_column('project', sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')))


def downgrade() -> None:
    pass
