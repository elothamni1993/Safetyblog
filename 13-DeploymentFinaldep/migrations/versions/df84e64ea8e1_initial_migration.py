"""Initial migration

Revision ID: df84e64ea8e1
Revises:
Create Date: 2024-10-05 17:51:35.580655

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = 'df84e64ea8e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Check if 'user' table exists
    conn = op.get_bind()
    inspector = inspect(conn)
    
    if 'user' not in inspector.get_table_names():
        op.create_table('user',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(length=20), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('image_file', sa.String(length=20), nullable=False),
            sa.Column('password', sa.String(length=60), nullable=False),
            sa.Column('confirmed', sa.Boolean(), nullable=True),
            sa.Column('role', sa.Integer(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email'),
            sa.UniqueConstraint('username')
        )
    
    # Create the other tables
    op.create_table('post',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('date_posted', sa.DateTime(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('picture', sa.String(length=20), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('comment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('date_posted', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('post_like',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('liked', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop the tables
    op.drop_table('post_like')
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('user')

