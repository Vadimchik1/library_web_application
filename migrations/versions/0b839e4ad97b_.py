"""empty message

Revision ID: 0b839e4ad97b
Revises: 
Create Date: 2021-04-30 20:29:17.412034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b839e4ad97b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('dtypesrecords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('menu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.Column('url_is_inner', sa.Boolean(), nullable=True),
    sa.Column('massiv_id', sa.PickleType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('partners',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('right_panel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=250), server_default='', nullable=False),
    sa.Column('active', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('confirmed_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('photo', sa.BLOB(), nullable=True),
    sa.Column('text', sa.TEXT(), nullable=True),
    sa.Column('disptype_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['disptype_id'], ['dtypesrecords.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('submenu',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.Column('url_is_inner', sa.Boolean(), nullable=True),
    sa.Column('menu_parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_parent_id'], ['menu.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.drop_table('submenu')
    op.drop_table('records')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('right_panel')
    op.drop_table('partners')
    op.drop_table('menu')
    op.drop_table('dtypesrecords')
    op.drop_table('categories')
    # ### end Alembic commands ###
