"""alter message table

Revision ID: 9f20295e490d
Revises: 14de824011d1
Create Date: 2023-11-05 11:10:48.635656

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9f20295e490d'
down_revision = '14de824011d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_column('subject')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('subject', mysql.VARCHAR(length=100), nullable=False))

    # ### end Alembic commands ###
