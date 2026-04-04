"""server_default TIMESTAMP for all tables

Revision ID: cc8d24fca387
Revises: 610633fe8292
Create Date: 2026-04-04 17:54:44.477572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'cc8d24fca387'
down_revision: Union[str, Sequence[str], None] = '610633fe8292'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'messages',
        'created_at',
        server_default=text("NOW()")
    )
    op.alter_column(
        'downloads',
        'created_at',
        server_default=text("NOW()")
    )
    op.alter_column(
        'projects',
        'created_at',
        server_default=text("NOW()")
    )
    op.alter_column(
        'users',
        'created_at',
        server_default=text("NOW()")
    )
    op.alter_column(
        'visits',
        'created_at',
        server_default=text("NOW()")
    )


def downgrade() -> None:
    op.alter_column(
        'messages',
        'created_at',
        server_default=None
    )
    op.alter_column(
        'downloads',
        'created_at',
        server_default=None
    )
    op.alter_column(
        'projects',
        'created_at',
        server_default=None
    )
    op.alter_column(
        'users',
        'created_at',
        server_default=None
    )
    op.alter_column(
        'visits',
        'created_at',
        server_default=None
    )
