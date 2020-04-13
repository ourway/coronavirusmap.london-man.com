"""create token column for users

Revision ID: 6466a14f4dfc
Revises: 
Create Date: 2020-04-13 17:27:20.033896

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = "6466a14f4dfc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user",
        sa.Column("token", sa.String, default=uuid4().hex, index=True, nullable=True),
    )


def downgrade():
    op.drop_column("user", "token")
