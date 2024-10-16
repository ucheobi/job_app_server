"""updated profile model

Revision ID: 8a7898e9da0f
Revises: 0b3072c3e90d
Create Date: 2024-10-16 20:16:31.917678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a7898e9da0f'
down_revision: Union[str, None] = '0b3072c3e90d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
