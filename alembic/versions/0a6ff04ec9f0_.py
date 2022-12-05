"""empty message

Revision ID: 0a6ff04ec9f0
Revises: c4bff44f6613
Create Date: 2022-12-05 14:19:24.599244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0a6ff04ec9f0'
down_revision = 'c4bff44f6613'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('role', sa.Enum('user', 'admin'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'role')
    # ### end Alembic commands ###