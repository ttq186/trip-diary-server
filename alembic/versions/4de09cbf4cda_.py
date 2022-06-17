"""empty message

Revision ID: 4de09cbf4cda
Revises: 3d587113a8d1
Create Date: 2022-06-17 19:02:04.760041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4de09cbf4cda'
down_revision = '3d587113a8d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('avatar_url', sa.String(), nullable=True),
    sa.Column('cover_img_url', sa.String(), nullable=True),
    sa.Column('is_female', sa.Boolean(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trip',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('cover_img_url', sa.String(), nullable=True),
    sa.Column('from_lat', sa.Float(), nullable=False),
    sa.Column('to_lat', sa.Float(), nullable=False),
    sa.Column('from_lng', sa.Float(), nullable=False),
    sa.Column('to_lng', sa.Float(), nullable=False),
    sa.Column('start_at', sa.Date(), nullable=False),
    sa.Column('back_trip_at', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_finished', sa.Boolean(), nullable=True),
    sa.Column('is_public', sa.Boolean(), nullable=True),
    sa.Column('can_be_reminded', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('scope', sa.Enum('ALL', 'GLOBAL', 'LOCAL', name='tripscope'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('checklist_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('has_prepared', sa.Boolean(), nullable=True),
    sa.Column('trip_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('review', sa.Text(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lng', sa.Float(), nullable=True),
    sa.Column('start_at', sa.Date(), nullable=True),
    sa.Column('trip_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trip_comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.Column('trip_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['trip_comment.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trip_like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trip_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['trip_id'], ['trip.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('location_file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('IMAGE', 'VIDEO', 'COMPRESS', name='filetype'), nullable=True),
    sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('location_file')
    op.drop_table('trip_like')
    op.drop_table('trip_comment')
    op.drop_table('location')
    op.drop_table('checklist_item')
    op.drop_table('trip')
    op.drop_table('user')
    # ### end Alembic commands ###