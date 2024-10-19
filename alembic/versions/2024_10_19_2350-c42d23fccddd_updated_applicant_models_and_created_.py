"""updated applicant models and created new job model

Revision ID: c42d23fccddd
Revises: f97b61b2e989
Create Date: 2024-10-19 23:50:25.176871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c42d23fccddd'
down_revision: Union[str, None] = 'f97b61b2e989'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
