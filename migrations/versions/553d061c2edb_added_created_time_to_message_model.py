"""added created time to message model

Revision ID: 553d061c2edb
Revises: deaaeba9e6ec
Create Date: 2022-03-10 17:06:21.865916

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '553d061c2edb'
down_revision = 'deaaeba9e6ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('created_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'created_at')
    # ### end Alembic commands ###