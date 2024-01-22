"""empty message

Revision ID: b7cad5a91a1a
Revises: 5edab0092cad
Create Date: 2024-01-15 17:30:48.688281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7cad5a91a1a'
down_revision = '5edab0092cad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('extra_fac_hourly_rate', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('extra_fac_complete_event_rate', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_column('extra_fac_complete_event_rate')
        batch_op.drop_column('extra_fac_hourly_rate')

    # ### end Alembic commands ###