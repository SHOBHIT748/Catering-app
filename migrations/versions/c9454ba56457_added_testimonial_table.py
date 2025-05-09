"""create testimonial table

Revision ID: c9454ba56457
Revises: 9ba4335ab82e
Create Date: 2025-04-15 09:09:41.528605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9454ba56457'
down_revision = '9ba4335ab82e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('testimonial',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),  # use lowercase and allow NULLs
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('testimonial')
    # ### end Alembic commands ###

