"""empty message

Revision ID: d185164b208e
Revises: 98664837b595
Create Date: 2022-02-18 14:06:12.124508

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd185164b208e'
down_revision = '98664837b595'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('VulList',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=128), nullable=True),
    sa.Column('pocname', sa.String(length=128), nullable=False),
    sa.Column('pocDesc', sa.Text(), nullable=True),
    sa.Column('references', sa.String(length=128), nullable=False),
    sa.Column('created', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scanTask',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pid', sa.String(length=128), nullable=False),
    sa.Column('tid', sa.String(length=128), nullable=False),
    sa.Column('url', sa.String(length=128), nullable=False),
    sa.Column('starttime', sa.String(length=30), nullable=False),
    sa.Column('endtime', sa.String(length=30), nullable=False),
    sa.Column('key', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scanTask')
    op.drop_table('VulList')
    # ### end Alembic commands ###
