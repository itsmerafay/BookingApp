"""empty message

Revision ID: d3570ae813b3
Revises: c8cacf794a48
Create Date: 2024-01-15 17:45:04.382550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3570ae813b3'
down_revision = 'c8cacf794a48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('allow_extra_fac_complete_event', sa.Boolean(), server_default='0', nullable=True))
        batch_op.add_column(sa.Column('allow_extra_fac_per_hour', sa.Boolean(), server_default='0', nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('allow_extra_fac_per_hour')
        batch_op.drop_column('allow_extra_fac_complete_event')

    # ### end Alembic commands ###
