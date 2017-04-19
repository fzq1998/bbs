"""empty message

Revision ID: 6cc89fd204a7
Revises: 02820ebab436
Create Date: 2017-04-15 13:42:05.103000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6cc89fd204a7'
down_revision = '02820ebab436'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('signin', sa.Column('is_sign_in', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('signin', 'is_sign_in')
    # ### end Alembic commands ###
