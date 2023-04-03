"""seed data

Revision ID: 3fdc234fea34
Revises: dfe094de545f
Create Date: 2023-04-03 12:33:38.989528

"""
from datetime import date
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3fdc234fea34'
down_revision = 'dfe094de545f'
branch_labels = None
depends_on = None


def upgrade():
    # ### Seed data ###

    op.execute("INSERT INTO users (id, username, email, password, created) VALUES ('7d0b64f2-3ac7-4bae-8397-55cf0e58aea1', 'johndoe', 'john@example.com', '$2b$12$TuXJmOwPDO80Cb5qOZopWeKCgTpjGapYDZZF7Nlh2mQDvj0xC2tJK', '2023-04-03 14:57:40.504480');")

    add_drones_sql = """
    INSERT INTO drones (id, serial_number, model, weight_limit, battery_capacity, state, created) VALUES 
    ('bb0e4ccd-ef49-48d5-a50a-a4574a931f7e', 'Drone1', 'Lightweight', '101', '24', 'RETURNING', '2023-04-02 20:36:21.942842'),
    ('26b269a5-0426-4fc1-8dde-a64a889e4fa6', 'Drone2', 'Lightweight', '400', '24', 'DELIVERED', '2023-04-02 20:38:01.208860'),
    ('d9662688-c3ab-4a58-b8d9-54e785c7633e', 'Drone3', 'Lightweight', '400', '24', 'DELIVERING', '2023-04-02 20:39:06.294592'),
    ('a2329c66-aa8f-4802-911f-2d80a8707ccc', 'Drone4', 'Lightweight', '400', '24', 'LOADED', '2023-04-02 20:43:55.982768'),
    ('68f13a2c-a6d8-41d4-9972-35a0e452251c', 'Drone5', 'Lightweight', '400', '24', 'IDLE', '2023-04-02 20:44:54.101563');
    """
    op.execute(add_drones_sql)


    # ### end Alembic commands ###


def downgrade():
    # Do nothing
    op.execute("DELETE FROM users WHERE id = '7d0b64f2-3ac7-4bae-8397-55cf0e58aea1';")

    delete_drones_sql = """
    DELETE FROM drones WHERE id in ('bb0e4ccd-ef49-48d5-a50a-a4574a931f7e', '26b269a5-0426-4fc1-8dde-a64a889e4fa6', 'd9662688-c3ab-4a58-b8d9-54e785c7633e', 'a2329c66-aa8f-4802-911f-2d80a8707ccc', '68f13a2c-a6d8-41d4-9972-35a0e452251c');
    """
    op.execute(delete_drones_sql)

    # ### end Alembic commands ###
