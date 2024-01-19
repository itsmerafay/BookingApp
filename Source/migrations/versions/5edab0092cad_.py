"""empty message

Revision ID: 5edab0092cad
Revises: 8c7a067fe792
Create Date: 2024-01-15 17:30:33.957968

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5edab0092cad'
down_revision = '8c7a067fe792'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('extra_fac_complete_event_rate')
        batch_op.drop_column('extra_fac_hourly_rate')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('extra_fac_hourly_rate', mysql.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('extra_fac_complete_event_rate', mysql.FLOAT(), nullable=True))

    # ### end Alembic commands ###
