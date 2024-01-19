"""empty message

Revision ID: 37a17a0a8ace
Revises: e885497c5747
Create Date: 2024-01-15 16:22:42.347531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37a17a0a8ace'
down_revision = 'e885497c5747'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('extra_fac_name', sa.String(length=1024), nullable=True))
        batch_op.add_column(sa.Column('extra_fac_image', sa.String(length=1024), nullable=True))
        batch_op.add_column(sa.Column('allow_extra_fac_complete_event', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('allow_extra_fac_per_hour', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('extra_fac_hourly_rate', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('extra_fac_complete_event_rate', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('extra_fac_complete_event_rate')
        batch_op.drop_column('extra_fac_hourly_rate')
        batch_op.drop_column('allow_extra_fac_per_hour')
        batch_op.drop_column('allow_extra_fac_complete_event')
        batch_op.drop_column('extra_fac_image')
        batch_op.drop_column('extra_fac_name')

    # ### end Alembic commands ###
