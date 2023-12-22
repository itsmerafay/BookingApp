"""empty message

Revision ID: 11d17aa63898
Revises: c2e63056794b
Create Date: 2023-12-20 15:40:52.453156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11d17aa63898'
down_revision = 'c2e63056794b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.alter_column('event_icon',
               existing_type=sa.BLOB(),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.alter_column('event_icon',
               existing_type=sa.String(length=255),
               type_=sa.BLOB(),
               existing_nullable=True)

    # ### end Alembic commands ###