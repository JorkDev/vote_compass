"""create core tables: questions, parties, answers, results

Revision ID: 0002_create_core_tables
Revises: 0001_create_users_table
Create Date: 2025-05-24 12:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002_create_core_tables'
down_revision = '0001_create_users_table'
branch_labels = None
depends_on = None


def upgrade():
    # questions
    op.create_table(
        'questions',
        sa.Column('id', sa.String(), primary_key=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('options', sa.JSON(), nullable=False),
        sa.Column('dimension', sa.String(), nullable=False),
        sa.Column('topic', sa.String(), nullable=False),
        sa.Column('additional_info', sa.Text(), nullable=True),
    )

    # parties
    op.create_table(
        'parties',
        sa.Column('party_id', sa.String(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('faction', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('inscription_date', sa.Date(), nullable=True),
        sa.Column('founder', sa.String(), nullable=True),
        sa.Column('current_leader', sa.String(), nullable=True),
        sa.Column('presidential_candidate', sa.String(), nullable=True),
        sa.Column('positions', sa.JSON(), nullable=False),
    )

    # answers
    op.create_table(
        'answers',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_id', sa.String(), nullable=False),
        sa.Column('choice', sa.Integer(), nullable=False),
        sa.Column('answered_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_answers_user_id', 'answers', ['user_id'])
    op.create_index('ix_answers_question_id', 'answers', ['question_id'])

    # results
    op.create_table(
        'results',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('data', sa.JSON(), nullable=False),
        sa.Column('token', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), unique=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index('ix_results_user_id', 'results', ['user_id'])
    op.create_index('ix_results_token', 'results', ['token'])


def downgrade():
    op.drop_index('ix_results_token', table_name='results')
    op.drop_index('ix_results_user_id', table_name='results')
    op.drop_table('results')

    op.drop_index('ix_answers_question_id', table_name='answers')
    op.drop_index('ix_answers_user_id', table_name='answers')
    op.drop_table('answers')

    op.drop_table('parties')
    op.drop_table('questions')
