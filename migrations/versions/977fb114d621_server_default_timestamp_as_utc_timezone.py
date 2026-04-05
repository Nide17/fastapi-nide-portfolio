"""server_default TIMESTAMP as UTC Timezone

Revision ID: 977fb114d621
Revises: cc8d24fca387
Create Date: 2026-04-05 10:40:40.823907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '977fb114d621'
down_revision: Union[str, Sequence[str], None] = 'cc8d24fca387'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.alter_column(
        'messages',
        'created_at',
        server_default=text("NOW() AT TIME ZONE 'UTC'")
    )
    op.alter_column(
        'downloads',
        'created_at',
        server_default=text("NOW() AT TIME ZONE 'UTC'")
    )
    op.alter_column(
        'projects',
        'created_at',
        server_default=text("NOW() AT TIME ZONE 'UTC'")
    )
    op.alter_column(
        'users',
        'created_at',
        server_default=text("NOW() AT TIME ZONE 'UTC'")
    )
    op.alter_column(
        'visits',
        'created_at',
        server_default=text("NOW() AT TIME ZONE 'UTC'")
    )


def downgrade() -> None:
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
