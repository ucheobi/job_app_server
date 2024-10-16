"""updated - adjusted owner id to be unique

Revision ID: 3aac4ddb1fda
Revises: 8a7898e9da0f
Create Date: 2024-10-16 22:45:59.158501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3aac4ddb1fda'
down_revision: Union[str, None] = '8a7898e9da0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
