"""convert_ids_to_uuid

Revision ID: a97a7c1757fa
Revises: df1f8b72d89f
Create Date: 2025-09-15 21:50:49.785963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a97a7c1757fa'
down_revision: Union[str, Sequence[str], None] = 'df1f8b72d89f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create extension for UUID support if not exists
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    
    # Create temporary UUID columns for primary keys
    op.add_column('users', sa.Column('new_id', sa.UUID(), nullable=True))
    op.add_column('chats', sa.Column('new_id', sa.UUID(), nullable=True))
    op.add_column('messages', sa.Column('new_id', sa.UUID(), nullable=True))
    op.add_column('documents', sa.Column('new_id', sa.UUID(), nullable=True))
    
    # Create temporary UUID columns for foreign keys
    op.add_column('chats', sa.Column('new_user_id', sa.UUID(), nullable=True))
    op.add_column('messages', sa.Column('new_chat_id', sa.UUID(), nullable=True))
    op.add_column('documents', sa.Column('new_user_id', sa.UUID(), nullable=True))
    
    # Generate UUIDs for primary keys
    connection = op.get_bind()
    connection.execute(sa.text("UPDATE users SET new_id = uuid_generate_v4()"))
    connection.execute(sa.text("UPDATE chats SET new_id = uuid_generate_v4()"))
    connection.execute(sa.text("UPDATE messages SET new_id = uuid_generate_v4()"))
    connection.execute(sa.text("UPDATE documents SET new_id = uuid_generate_v4()"))
    
    # Get existing foreign key constraints and drop them
    inspector = sa.inspect(connection)
    for table in ['chats', 'messages', 'documents']:
        for fk in inspector.get_foreign_keys(table):
            op.drop_constraint(fk['name'], table, type_='foreignkey')
    
    # Update foreign key references
    connection.execute(sa.text("""
        UPDATE chats c
        SET new_user_id = u.new_id
        FROM users u
        WHERE c.user_id = u.id
    """))
    
    connection.execute(sa.text("""
        UPDATE messages m
        SET new_chat_id = c.new_id
        FROM chats c
        WHERE m.chat_id = c.id
    """))
    
    connection.execute(sa.text("""
        UPDATE documents d
        SET new_user_id = u.new_id
        FROM users u
        WHERE d.user_id = u.id
    """))
    
    # Drop old primary key columns
    op.drop_column('users', 'id')
    op.drop_column('chats', 'id')
    op.drop_column('messages', 'id')
    op.drop_column('documents', 'id')
    
    # Rename new UUID columns
    op.alter_column('users', 'new_id', new_column_name='id', nullable=False)
    op.alter_column('chats', 'new_id', new_column_name='id', nullable=False)
    op.alter_column('messages', 'new_id', new_column_name='id', nullable=False)
    op.alter_column('documents', 'new_id', new_column_name='id', nullable=False)
    
    # Drop old foreign key columns
    op.drop_column('chats', 'user_id')
    op.drop_column('messages', 'chat_id')
    op.drop_column('documents', 'user_id')
    
    # Rename new foreign key columns
    op.alter_column('chats', 'new_user_id', new_column_name='user_id', nullable=False)
    op.alter_column('messages', 'new_chat_id', new_column_name='chat_id', nullable=False)
    op.alter_column('documents', 'new_user_id', new_column_name='user_id', nullable=False)
    
    # Create primary key constraints
    op.create_primary_key('users_pkey', 'users', ['id'])
    op.create_primary_key('chats_pkey', 'chats', ['id'])
    op.create_primary_key('messages_pkey', 'messages', ['id'])
    op.create_primary_key('documents_pkey', 'documents', ['id'])
    
    # Create foreign key constraints
    op.create_foreign_key('chats_user_id_fkey', 'chats', 'users', ['user_id'], ['id'])
    op.create_foreign_key('messages_chat_id_fkey', 'messages', 'chats', ['chat_id'], ['id'])
    op.create_foreign_key('documents_user_id_fkey', 'documents', 'users', ['user_id'], ['id'])
    op.alter_column('chats', 'user_id',
               existing_type=sa.INTEGER(),
               type_=sa.UUID(),
               existing_nullable=False)
    op.alter_column('documents', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.UUID(),
               existing_nullable=False)
    op.alter_column('documents', 'user_id',
               existing_type=sa.INTEGER(),
               type_=sa.UUID(),
               nullable=False)
    op.alter_column('messages', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.UUID(),
               existing_nullable=False)
    op.alter_column('messages', 'chat_id',
               existing_type=sa.INTEGER(),
               type_=sa.UUID(),
               existing_nullable=False)
    op.alter_column('users', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.UUID(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('messages', 'chat_id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('messages', 'id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('documents', 'user_id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               nullable=True)
    op.alter_column('documents', 'id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('chats', 'user_id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('chats', 'id',
               existing_type=sa.UUID(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               existing_server_default=sa.text("nextval('chats_id_seq'::regclass)"))
    # ### end Alembic commands ###
