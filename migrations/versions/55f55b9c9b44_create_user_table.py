"""create user table

Revision ID: 55f55b9c9b44
Revises: 
Create Date: 2023-02-26 22:22:56.200966

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import column, func, table


# revision identifiers, used by Alembic.
revision = '55f55b9c9b44'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.String(length=20), nullable=False, unique=True),
        sa.Column("email_address", sa.String(length=100), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=False, default=func.now()
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=False, default=func.now()
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    user_table = table(
        "users",
        column("id", sa.Integer),
        column('user_id', sa.String),
        column('email_address', sa.String),
        column('password', sa.String),
        column('role', sa.String),
        column('created_at', sa.DateTime),
        column('updated_at', sa.DateTime),
    )

    now = datetime.utcnow()

    op.bulk_insert(
        user_table,
        [
            {
                "id": 1,
                "user_id": "superuser",
                "email_address": "my-email@abc.def",
                "password": "$2b$12$EU/VnZ7KVayTcG3QMtGwyO29DBQ.P2T/SMh2P3uz.St8.HkkEu2Sm",
                "role": "superuser",
                "created_at": now,
                "updated_at": now
            }
        ]
    )


def downgrade() -> None:
    op.drop_table("alerts")
