"""Add Job model

Revision ID: fd6ce52b5909
Revises: 
Create Date: 2024-12-15 13:48:32.317078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd6ce52b5909'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_title', sa.String(length=120), nullable=False),
    sa.Column('company_name', sa.String(length=120), nullable=False),
    sa.Column('location', sa.String(length=120), nullable=False),
    sa.Column('responsibilities', sa.Text(), nullable=False),
    sa.Column('requirements', sa.Text(), nullable=False),
    sa.Column('raw_jd_text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_job_job_title'), ['job_title'], unique=False)
        batch_op.create_index(batch_op.f('ix_job_location'), ['location'], unique=False)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('resume_text', sa.Text(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_job_location'))
        batch_op.drop_index(batch_op.f('ix_job_job_title'))

    op.drop_table('job')
    # ### end Alembic commands ###
