"""updated company and job seeker  models

Revision ID: f97b61b2e989
Revises: d90d600d9cc8
Create Date: 2024-10-18 13:32:57.680395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f97b61b2e989'
down_revision: Union[str, None] = 'd90d600d9cc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
