"""DataBase init

Revision ID: ffb8c3a770a1
Revises: 
Create Date: 2023-02-18 01:26:45.271174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ffb8c3a770a1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "permission_object",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_permission_object")),
        sa.UniqueConstraint("id", name=op.f("uq_permission_object_id")),
        sa.UniqueConstraint("name", name=op.f("uq_permission_object_name")),
    )
    op.create_table(
        "role",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_role")),
        sa.UniqueConstraint("id", name=op.f("uq_role_id")),
        sa.UniqueConstraint("name", name=op.f("uq_role_name")),
    )
    op.create_table(
        "user",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("id", name=op.f("uq_user_id")),
        sa.UniqueConstraint("username", name=op.f("uq_user_username")),
    )
    op.create_table(
        "auth_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("device", sa.Text(), nullable=False),
        sa.Column("datetime", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("endpoint", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_auth_history_user_id_user")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_auth_history")),
        sa.UniqueConstraint("id", name=op.f("uq_auth_history_id")),
    )
    op.create_table(
        "permission",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("permission_object_id", sa.UUID(), nullable=True),
        sa.Column("role_id", sa.UUID(), nullable=True),
        sa.Column("permitted_action", sa.String(length=24), nullable=True),
        sa.Column("object_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(
            ["permission_object_id"],
            ["permission_object.id"],
            name=op.f("fk_permission_permission_object_id_permission_object"),
        ),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"], name=op.f("fk_permission_role_id_role")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_permission")),
        sa.UniqueConstraint("id", name=op.f("uq_permission_id")),
    )
    op.create_table(
        "user_role",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("role_id", sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(["role_id"], ["role.id"], name=op.f("fk_user_role_role_id_role")),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name=op.f("fk_user_role_user_id_user")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_role")),
        sa.UniqueConstraint("id", name=op.f("uq_user_role_id")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_role")
    op.drop_table("permission")
    op.drop_table("auth_history")
    op.drop_table("user")
    op.drop_table("role")
    op.drop_table("permission_object")
    # ### end Alembic commands ###
