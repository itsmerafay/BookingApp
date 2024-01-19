"""empty message

Revision ID: 72469529771e
Revises: 237f693cc7a0
Create Date: 2024-01-18 15:44:38.820687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72469529771e'
down_revision = '237f693cc7a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vendor', schema=None) as batch_op:
        batch_op.add_column(sa.Column('wallet', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vendor', schema=None) as batch_op:
        batch_op.drop_column('wallet')

    # ### end Alembic commands ###
