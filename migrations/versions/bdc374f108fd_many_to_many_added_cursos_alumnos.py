"""many to many added, cursos-alumnos

Revision ID: bdc374f108fd
Revises: 4542a6dd72d5
Create Date: 2021-06-07 16:03:55.374970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdc374f108fd'
down_revision = '4542a6dd72d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario_curso',
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_curso', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_curso'], ['curso.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id_user', 'id_curso')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuario_curso')
    # ### end Alembic commands ###