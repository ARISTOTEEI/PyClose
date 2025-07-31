"""empty message

Revision ID: 82e901d472a0
Revises: 9177fed3dee1
Create Date: 2025-07-31 17:02:05.187244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '82e901d472a0'
down_revision: Union[str, Sequence[str], None] = 'e43eefdb246b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
