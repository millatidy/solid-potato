"""empty message

Revision ID: ece415fe4a9b
Revises: e10ec7dce2ea
Create Date: 2019-04-30 01:50:58.170648

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ece415fe4a9b'
down_revision = 'e10ec7dce2ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('feature', sa.Column('suspended', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('feature', 'suspended')
    # ### end Alembic commands ###
