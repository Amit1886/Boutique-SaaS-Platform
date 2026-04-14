"""designer progress

Revision ID: 0002_designer_progress
Revises: 0001_initial
Create Date: 2026-04-14
"""

from alembic import op
import sqlalchemy as sa

revision = "0002_designer_progress"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "designer_progress",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("progress", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_designer_progress_user_id", "designer_progress", ["user_id"], unique=True)


def downgrade():
    op.drop_index("ix_designer_progress_user_id", table_name="designer_progress")
    op.drop_table("designer_progress")

