"""empty message

Revision ID: b0ce941f79b7
Revises: a13314efe3af
Create Date: 2024-01-19 19:24:58.855945

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0ce941f79b7'
down_revision = 'a13314efe3af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_type', sa.String(length=10), nullable=False),
    sa.Column('transaction_time', sa.DateTime(), nullable=False),
    sa.Column('transaction_amount', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    # ### end Alembic commands ###
