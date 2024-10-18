"""updated recruiter models

Revision ID: d90d600d9cc8
Revises: 3aac4ddb1fda
Create Date: 2024-10-18 13:23:25.577919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd90d600d9cc8'
down_revision: Union[str, None] = '3aac4ddb1fda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
