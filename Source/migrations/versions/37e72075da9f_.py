"""empty message

Revision ID: 37e72075da9f
Revises: 
Create Date: 2023-12-07 15:10:59.718290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37e72075da9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cancelled', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_column('cancelled')

    # ### end Alembic commands ###
