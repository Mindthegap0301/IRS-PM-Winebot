"""create options table

Revision ID: 511f00ea5d21
Revises: 3cda552c5044
Create Date: 2023-04-05 20:50:44.958677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '511f00ea5d21'
down_revision = '3cda552c5044'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('options',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.Column('data_type', sa.Enum('string', 'number', name='datatype'), nullable=False),
    sa.Column('label', sa.String(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('options')
    # ### end Alembic commands ###
