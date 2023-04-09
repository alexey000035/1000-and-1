"""Longtext for 'page' table in mysql

Revision ID: 42a9f0496347
Revises: fc744f8e7398
Create Date: 2016-11-23 09:11:19.712613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42a9f0496347'
down_revision = 'fc744f8e7398'
branch_labels = None
depends_on = None


def upgrade():
    # Warning: sqlite dont support such field types
    # to avoid errors y must either comment this lines for SQLite and uncomment after
    # or to initialize SQLite with imit/seed.py script
    op.alter_column('page', 'text_ru', type_=sa.UnicodeText(4294967295))
    op.alter_column('page', 'text_en', type_=sa.UnicodeText(4294967295))


def downgrade():
    op.alter_column('page', 'text_ru', type_=sa.Text())
    op.alter_column('page', 'text_en', type_=sa.Text())
