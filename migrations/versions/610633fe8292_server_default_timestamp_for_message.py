"""server_default TIMESTAMP for message

Revision ID: 610633fe8292
Revises: a4977dfbf47c
Create Date: 2026-04-04 17:47:54.004957

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '610633fe8292'
down_revision: Union[str, Sequence[str], None] = 'a4977dfbf47c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'messages',
        'created_at',
        server_default=text("NOW()")
    )


def downgrade() -> None:
    op.alter_column(
        'messages',
        'created_at',
        server_default=None
    )

