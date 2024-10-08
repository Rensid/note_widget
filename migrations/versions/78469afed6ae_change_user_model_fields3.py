"""change user model fields3

Revision ID: 78469afed6ae
Revises: 1cf4f7060954
Create Date: 2024-09-18 20:09:29.381763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78469afed6ae'
down_revision: Union[str, None] = '1cf4f7060954'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('note', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.drop_constraint('note_user_id_fkey', 'note', type_='foreignkey')
    op.create_foreign_key(None, 'note', 'user', ['owner_id'], ['id'])
    op.drop_column('note', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('note', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'note', type_='foreignkey')
    op.create_foreign_key('note_user_id_fkey', 'note', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('note', 'owner_id')
    # ### end Alembic commands ###
