from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9ba4335ab82e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Rename the old table
    op.execute('ALTER TABLE menu RENAME TO menu_old')

    # Create a new table without the 'service_id' column
    op.create_table(
        'menu',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text),
    )

    # Copy data from old table to new table (assuming columns match)
    op.execute('INSERT INTO menu (id, name, description) SELECT id, name, description FROM menu_old')

    # Drop the old table
    op.execute('DROP TABLE menu_old')


def downgrade():
    # Restore the old table if necessary
    op.execute('ALTER TABLE menu RENAME TO menu_old')

