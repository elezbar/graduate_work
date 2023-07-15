"""Add action col to AuthHistory

Revision ID: 55132cd55ce9
Revises: ffb8c3a770a1
Create Date: 2023-02-25 01:53:37.154368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "55132cd55ce9"
down_revision = "ffb8c3a770a1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("auth_history", sa.Column("action", sa.String))


def downgrade() -> None:
    op.drop_column("auth_history", "action")
