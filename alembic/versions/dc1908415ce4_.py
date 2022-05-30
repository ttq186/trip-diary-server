"""empty message

Revision ID: dc1908415ce4
Revises: 3a5b6be03c85
Create Date: 2022-05-30 22:13:41.141142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc1908415ce4'
down_revision = '3a5b6be03c85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('review', sa.Text(), nullable=False))
    op.drop_column('location', 'reivew')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('location', sa.Column('reivew', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('location', 'review')
    # ### end Alembic commands ###
