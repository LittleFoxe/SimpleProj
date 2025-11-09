"""create_incident_table

Revision ID: 001
Revises: 

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# Идентификаторы версии
revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Создание таблицы Incidents
    op.create_table('incidents',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True, autoincrement=True),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('status', sa.Text(), nullable=False),
        sa.Column('source', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.CheckConstraint(
            "status IN ('pending', 'solved', 'in progress')", 
            name='ck_incident_status'
        ),
        sa.CheckConstraint(
            "source IN ('operator', 'monitoring', 'partner')", 
            name='ck_incident_source'
        )
    )

    # Функция для создания начальной даты
    created_at_date = lambda seconds: datetime(2025, 11, 9, 10, 30, seconds)

    # Добавление начальных данных
    op.bulk_insert(
        sa.table('incidents',
            sa.column('text', sa.Text),
            sa.column('status', sa.Text),
            sa.column('source', sa.Text),
            sa.column('created_at', sa.DateTime)
        ),
        [
            {
                'text': f'Самокат номер {i} не в сети!',
                'status': 'pending' if i > 5 else 'in progress' if i > 2 else 'solved',
                'source': 'monitoring' if i % 2 == 0 else 'partner',
                'created_at': created_at_date(i)
            } for i in range(1, 11)
        ]
    )

def downgrade():
    op.drop_table('incidents')