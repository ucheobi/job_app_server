"""added more job features

Revision ID: 70dee3d1f38a
Revises: c42d23fccddd
Create Date: 2024-12-22 00:08:02.947632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70dee3d1f38a'
down_revision: Union[str, None] = 'c42d23fccddd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
