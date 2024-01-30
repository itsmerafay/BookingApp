"""empty message

Revision ID: 5574c2a161b4
Revises: bb3c52776153
Create Date: 2024-01-30 16:45:59.069752

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5574c2a161b4'
down_revision = 'bb3c52776153'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_constraint('booking_ibfk_3', type_='foreignkey')
        batch_op.drop_column('extra_facility_id')

    with op.batch_alter_table('booking_extra_facility', schema=None) as batch_op:
        batch_op.alter_column('quantity',
               existing_type=mysql.FLOAT(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking_extra_facility', schema=None) as batch_op:
        batch_op.alter_column('quantity',
               existing_type=mysql.FLOAT(),
               nullable=True)

    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('extra_facility_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('booking_ibfk_3', 'extra_facility', ['extra_facility_id'], ['id'])

    # ### end Alembic commands ###
