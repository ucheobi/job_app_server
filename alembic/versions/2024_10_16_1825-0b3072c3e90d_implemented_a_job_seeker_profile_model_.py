"""implemented a job seeker profile model and endpoint

Revision ID: 0b3072c3e90d
Revises: 3bf626d199af
Create Date: 2024-10-16 18:25:41.395205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b3072c3e90d'
down_revision: Union[str, None] = '3bf626d199af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
