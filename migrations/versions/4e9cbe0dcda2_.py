"""empty message

Revision ID: 4e9cbe0dcda2
Revises: e96989d251e8
Create Date: 2020-01-26 20:10:47.850556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e9cbe0dcda2'
down_revision = 'e96989d251e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('projects', sa.Column('demo', sa.String(length=120), nullable=True))
    op.add_column('projects', sa.Column('github', sa.String(length=120), nullable=True))
    op.drop_index('image', table_name='projects')
    op.create_unique_constraint(None, 'projects', ['demo'])
    op.create_unique_constraint(None, 'projects', ['github'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'projects', type_='unique')
    op.drop_constraint(None, 'projects', type_='unique')
    op.create_index('image', 'projects', ['image'], unique=True)
    op.drop_column('projects', 'github')
    op.drop_column('projects', 'demo')
    # ### end Alembic commands ###