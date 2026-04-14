"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-14
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=190), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False, server_default=""),
        sa.Column("language", sa.String(length=5), nullable=False, server_default="en"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("category", sa.String(length=40), nullable=False),
        sa.Column("image_url", sa.String(length=500), nullable=False, server_default=""),
        sa.Column("base_color", sa.String(length=40), nullable=False, server_default="pink"),
        sa.Column("fabric", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("style_tag", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("mood_tag", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("price", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "favorites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "product_id", name="uq_fav_user_product"),
    )
    op.create_index("ix_favorites_user_id", "favorites", ["user_id"])
    op.create_index("ix_favorites_product_id", "favorites", ["product_id"])

    op.create_table(
        "trylist",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("user_id", "product_id", name="uq_try_user_product"),
    )
    op.create_index("ix_trylist_user_id", "trylist", ["user_id"])
    op.create_index("ix_trylist_product_id", "trylist", ["product_id"])

    op.create_table(
        "moodboards",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(length=40), nullable=False),
        sa.Column("name_en", sa.String(length=60), nullable=False),
        sa.Column("name_hi", sa.String(length=60), nullable=False),
        sa.Column("theme_color", sa.String(length=20), nullable=False),
        sa.Column("banner", sa.String(length=200), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_moodboards_key", "moodboards", ["key"], unique=True)

    op.create_table(
        "user_moods",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("mood_key", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_user_moods_user_id", "user_moods", ["user_id"], unique=True)

    op.create_table(
        "personality_tests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column("result_key", sa.String(length=60), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_personality_tests_user_id", "personality_tests", ["user_id"])

    op.create_table(
        "style_profiles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("personality_key", sa.String(length=80), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_style_profiles_user_id", "style_profiles", ["user_id"], unique=True)

    op.create_table(
        "user_feed",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("product_ids", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_user_feed_user_id", "user_feed", ["user_id"])


def downgrade():
    op.drop_index("ix_user_feed_user_id", table_name="user_feed")
    op.drop_table("user_feed")
    op.drop_index("ix_style_profiles_user_id", table_name="style_profiles")
    op.drop_table("style_profiles")
    op.drop_index("ix_personality_tests_user_id", table_name="personality_tests")
    op.drop_table("personality_tests")
    op.drop_index("ix_user_moods_user_id", table_name="user_moods")
    op.drop_table("user_moods")
    op.drop_index("ix_moodboards_key", table_name="moodboards")
    op.drop_table("moodboards")
    op.drop_index("ix_trylist_product_id", table_name="trylist")
    op.drop_index("ix_trylist_user_id", table_name="trylist")
    op.drop_table("trylist")
    op.drop_index("ix_favorites_product_id", table_name="favorites")
    op.drop_index("ix_favorites_user_id", table_name="favorites")
    op.drop_table("favorites")
    op.drop_table("products")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

