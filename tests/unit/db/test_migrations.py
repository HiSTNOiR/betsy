"""
Tests for the database migration system.

This module tests the functionality of the migration system.
"""

import os
import shutil
import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path
from unittest import mock

import pytest

from bot.db.connection import Database
from bot.db.migrations import (
    Migration, SQLMigration, MigrationManager, MigrationInfo,
    MigrationError, MigrationApplyError, MigrationRollbackError,
    initialise_migration_manager, migrate_database, rollback_database,
    get_database_version, create_migration
)


@pytest.fixture
def temp_db_path():
    """Create a temporary database path."""
    # Create a temporary file for the database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    yield db_path

    # Clean up
    try:
        os.unlink(db_path)
    except OSError:
        pass


@pytest.fixture
def temp_migrations_dir():
    """Create a temporary migrations directory."""
    # Create a temporary directory for migrations
    migrations_dir = tempfile.mkdtemp()

    yield migrations_dir

    # Clean up
    try:
        shutil.rmtree(migrations_dir)
    except OSError:
        pass


@pytest.fixture
def db(temp_db_path):
    """Create a test database."""
    # Create a database instance with the temporary path
    database = Database(temp_db_path)

    yield database

    # Clean up
    database.close_all()


@pytest.fixture
def migration_manager(db, temp_migrations_dir):
    """Create a migration manager with a temporary database and migrations directory."""
    # Create a migration manager
    manager = MigrationManager(db, temp_migrations_dir)

    yield manager


def create_test_migration_file(dir_path, version, name, up_sql, down_sql=None):
    """Helper function to create a test migration file."""
    # Ensure directory exists
    os.makedirs(dir_path, exist_ok=True)

    # Create up SQL file
    file_name = f"{version:04d}_{name}.sql"
    file_path = os.path.join(dir_path, file_name)

    with open(file_path, 'w') as f:
        f.write(up_sql)

    # Create down SQL file if provided
    if down_sql:
        down_file_name = f"{version:04d}_{name}.down.sql"
        down_file_path = os.path.join(dir_path, down_file_name)

        with open(down_file_path, 'w') as f:
            f.write(down_sql)

    return file_path


class TestMigration:
    """Tests for the Migration base class."""

    def test_base_migration_requires_implementation(self):
        """Test that the base Migration class requires implementation of up() and down()."""
        # Create a migration with a mock database
        db_mock = mock.MagicMock()
        migration = Migration(db_mock)

        # Test that up() raises NotImplementedError
        with pytest.raises(NotImplementedError, match="Subclasses must implement up()"):
            migration.up()

        # Test that down() raises NotImplementedError
        with pytest.raises(NotImplementedError, match="Subclasses must implement down()"):
            migration.down()


class TestSQLMigration:
    """Tests for the SQLMigration class."""

    def test_up_executes_sql(self, db):
        """Test that the up() method executes the provided SQL."""
        # Create a SQL migration
        up_sql = "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT);"
        migration = SQLMigration(db, up_sql)

        # Apply the migration
        migration.up()

        # Verify that the table was created
        assert db.table_exists("test_table")

    def test_up_handles_multiple_statements(self, db):
        """Test that the up() method handles multiple SQL statements."""
        # Create a SQL migration with multiple statements
        up_sql = """
        CREATE TABLE test_table_1 (id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE test_table_2 (id INTEGER PRIMARY KEY, name TEXT);
        """
        migration = SQLMigration(db, up_sql)

        # Apply the migration
        migration.up()

        # Verify that both tables were created
        assert db.table_exists("test_table_1")
        assert db.table_exists("test_table_2")

    def test_down_executes_sql(self, db):
        """Test that the down() method executes the provided SQL."""
        # Create a SQL migration with up and down SQL
        up_sql = "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT);"
        down_sql = "DROP TABLE test_table;"
        migration = SQLMigration(db, up_sql, down_sql)

        # Apply the migration
        migration.up()

        # Verify that the table was created
        assert db.table_exists("test_table")

        # Roll back the migration
        migration.down()

        # Verify that the table was dropped
        assert not db.table_exists("test_table")

    def test_down_raises_error_if_no_down_sql(self, db):
        """Test that the down() method raises an error if no down SQL is provided."""
        # Create a SQL migration with no down SQL
        up_sql = "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT);"
        migration = SQLMigration(db, up_sql)

        # Apply the migration
        migration.up()

        # Try to roll back the migration
        with pytest.raises(MigrationRollbackError, match="No rollback SQL provided"):
            migration.down()


class TestMigrationManager:
    """Tests for the MigrationManager class."""

    def test_create_migrations_table(self, db, temp_migrations_dir):
        """Test that the migration manager creates the migrations table."""
        # Create a migration manager
        manager = MigrationManager(db, temp_migrations_dir)

        # Verify that the migrations table was created
        assert db.table_exists(manager.MIGRATIONS_TABLE)

    def test_get_applied_migrations_empty(self, migration_manager):
        """Test getting applied migrations when none have been applied."""
        # Get applied migrations
        migrations = migration_manager.get_applied_migrations()

        # Verify that no migrations are returned
        assert len(migrations) == 0

    def test_get_available_migrations_empty(self, migration_manager):
        """Test getting available migrations when none are available."""
        # Get available migrations
        migrations = migration_manager.get_available_migrations()

        # Verify that no migrations are returned
        assert len(migrations) == 0

    def test_get_available_migrations(self, migration_manager, temp_migrations_dir):
        """Test getting available migrations."""
        # Create some migration files
        create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )
        create_test_migration_file(
            temp_migrations_dir, 2, "create_items",
            "CREATE TABLE items (id INTEGER PRIMARY KEY);",
            "DROP TABLE items;"
        )

        # Get available migrations
        migrations = migration_manager.get_available_migrations()

        # Verify that the migrations are returned
        assert len(migrations) == 2
        assert 1 in migrations
        assert 2 in migrations
        assert migrations[1].name == "create_users"
        assert migrations[2].name == "create_items"

    def test_get_pending_migrations(self, migration_manager, temp_migrations_dir):
        """Test getting pending migrations."""
        # Create some migration files
        create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )
        create_test_migration_file(
            temp_migrations_dir, 2, "create_items",
            "CREATE TABLE items (id INTEGER PRIMARY KEY);",
            "DROP TABLE items;"
        )

        # Get pending migrations
        migrations = migration_manager.get_pending_migrations()

        # Verify that the migrations are returned
        assert len(migrations) == 2
        assert migrations[0].version == 1
        assert migrations[1].version == 2

    def test_apply_migration(self, migration_manager, db, temp_migrations_dir):
        """Test applying a migration."""
        # Create a migration file
        file_path = create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )

        # Get the migration info
        migration_info = MigrationInfo(
            version=1,
            name="create_users",
            file_path=file_path
        )

        # Apply the migration
        migration_manager.apply_migration(migration_info)

        # Verify that the migration was applied
        assert db.table_exists("users")

        # Verify that the migration was recorded
        applied_migrations = migration_manager.get_applied_migrations()
        assert 1 in applied_migrations
        assert applied_migrations[1].name == "create_users"

    def test_rollback_migration(self, migration_manager, db, temp_migrations_dir):
        """Test rolling back a migration."""
        # Create a migration file
        file_path = create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )

        # Get the migration info
        migration_info = MigrationInfo(
            version=1,
            name="create_users",
            file_path=file_path
        )

        # Apply the migration
        migration_manager.apply_migration(migration_info)

        # Verify that the migration was applied
        assert db.table_exists("users")

        # Roll back the migration
        migration_manager.rollback_migration(migration_info)

        # Verify that the migration was rolled back
        assert not db.table_exists("users")

        # Verify that the migration record was removed
        applied_migrations = migration_manager.get_applied_migrations()
        assert 1 not in applied_migrations

    def test_migrate(self, migration_manager, db, temp_migrations_dir):
        """Test migrating to the latest version."""
        # Create some migration files
        create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )
        create_test_migration_file(
            temp_migrations_dir, 2, "create_items",
            "CREATE TABLE items (id INTEGER PRIMARY KEY);",
            "DROP TABLE items;"
        )

        # Migrate
        applied_migrations = migration_manager.migrate()

        # Verify that both migrations were applied
        assert len(applied_migrations) == 2
        assert db.table_exists("users")
        assert db.table_exists("items")

        # Verify that the migrations were recorded
        applied_migrations = migration_manager.get_applied_migrations()
        assert 1 in applied_migrations
        assert 2 in applied_migrations

    def test_migrate_to_target_version(self, migration_manager, db, temp_migrations_dir):
        """Test migrating to a specific version."""
        # Create some migration files
        create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )
        create_test_migration_file(
            temp_migrations_dir, 2, "create_items",
            "CREATE TABLE items (id INTEGER PRIMARY KEY);",
            "DROP TABLE items;"
        )
        create_test_migration_file(
            temp_migrations_dir, 3, "create_orders",
            "CREATE TABLE orders (id INTEGER PRIMARY KEY);",
            "DROP TABLE orders;"
        )

        # Migrate to version 2
        applied_migrations = migration_manager.migrate(target_version=2)

        # Verify that only the first two migrations were applied
        assert len(applied_migrations) == 2
        assert db.table_exists("users")
        assert db.table_exists("items")
        assert not db.table_exists("orders")

        # Verify that the migrations were recorded
        applied_migrations = migration_manager.get_applied_migrations()
        assert 1 in applied_migrations
        assert 2 in applied_migrations
        assert 3 not in applied_migrations

    def test_rollback(self, migration_manager, db, temp_migrations_dir):
        """Test rolling back migrations."""
        # Create some migration files
        create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )
        create_test_migration_file(
            temp_migrations_dir, 2, "create_items",
            "CREATE TABLE items (id INTEGER PRIMARY KEY);",
            "DROP TABLE items;"
        )

        # Apply migrations
        migration_manager.migrate()

        # Verify that both migrations were applied
        assert db.table_exists("users")
        assert db.table_exists("items")

        # Roll back one migration
        rolled_back = migration_manager.rollback(steps=1)

        # Verify that only the last migration was rolled back
        assert len(rolled_back) == 1
        assert rolled_back[0].version == 2
        assert db.table_exists("users")
        assert not db.table_exists("items")

        # Verify that the migration record was removed
        applied_migrations = migration_manager.get_applied_migrations()
        assert 1 in applied_migrations
        assert 2 not in applied_migrations

    def test_migrate_to_version(self, migration_manager, db, temp_migrations_dir):
        """Test migrating to a specific version in either direction."""
        # Create some migration files
        create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )
        create_test_migration_file(
            temp_migrations_dir, 2, "create_items",
            "CREATE TABLE items (id INTEGER PRIMARY KEY);",
            "DROP TABLE items;"
        )
        create_test_migration_file(
            temp_migrations_dir, 3, "create_orders",
            "CREATE TABLE orders (id INTEGER PRIMARY KEY);",
            "DROP TABLE orders;"
        )

        # Migrate to version 3 (all migrations)
        migration_manager.migrate()

        # Verify that all migrations were applied
        assert db.table_exists("users")
        assert db.table_exists("items")
        assert db.table_exists("orders")

        # Migrate to version 1 (roll back to version 1)
        applied, rolled_back = migration_manager.migrate_to_version(1)

        # Verify that migrations 2 and 3 were rolled back
        assert len(applied) == 0
        assert len(rolled_back) == 2
        assert rolled_back[0].version == 3
        assert rolled_back[1].version == 2
        assert db.table_exists("users")
        assert not db.table_exists("items")
        assert not db.table_exists("orders")

        # Migrate to version 3 again (apply migrations 2 and 3)
        applied, rolled_back = migration_manager.migrate_to_version(3)

        # Verify that migrations 2 and 3 were applied
        assert len(applied) == 2
        assert len(rolled_back) == 0
        assert applied[0].version == 2
        assert applied[1].version == 3
        assert db.table_exists("users")
        assert db.table_exists("items")
        assert db.table_exists("orders")

    def test_get_current_version(self, migration_manager, temp_migrations_dir):
        """Test getting the current version."""
        # Initially, should be 0
        assert migration_manager.get_current_version() == 0

        # Create a migration file
        create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )

        # Apply the migration
        migration_manager.migrate()

        # Version should now be 1
        assert migration_manager.get_current_version() == 1

        # Create another migration file
        create_test_migration_file(
            temp_migrations_dir, 2, "create_items",
            "CREATE TABLE items (id INTEGER PRIMARY KEY);",
            "DROP TABLE items;"
        )

        # Apply the migration
        migration_manager.migrate()

        # Version should now be 2
        assert migration_manager.get_current_version() == 2

    def test_create_migration(self, migration_manager, temp_migrations_dir):
        """Test creating a new migration."""
        # Create a migration
        up_sql = "CREATE TABLE test_table (id INTEGER PRIMARY KEY);"
        down_sql = "DROP TABLE test_table;"
        migration_info = migration_manager.create_migration(
            "test_migration", up_sql, down_sql)

        # Verify that the migration was created
        assert migration_info.version == 1
        assert migration_info.name == "test_migration"

        # Verify that the migration files were created
        up_file = Path(temp_migrations_dir) / "0001_test_migration.sql"
        down_file = Path(temp_migrations_dir) / "0001_test_migration.down.sql"
        assert up_file.exists()
        assert down_file.exists()

        # Verify the file contents
        with open(up_file, 'r') as f:
            assert f.read() == up_sql
        with open(down_file, 'r') as f:
            assert f.read() == down_sql


class TestHelperFunctions:
    """Tests for the helper functions."""

    def test_initialise_migration_manager(self, db, temp_migrations_dir):
        """Test initialising the migration manager."""
        # Initialise the migration manager
        manager = initialise_migration_manager(temp_migrations_dir, db)

        # Verify that a migration manager was returned
        assert isinstance(manager, MigrationManager)

    def test_migrate_database(self, db, temp_migrations_dir):
        """Test migrating the database."""
        # Create a migration file
        create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )

        # Migrate the database
        applied_migrations = migrate_database(None, temp_migrations_dir, db)

        # Verify that the migration was applied
        assert len(applied_migrations) == 1
        assert applied_migrations[0].version == 1
        assert db.table_exists("users")

    def test_rollback_database(self, db, temp_migrations_dir):
        """Test rolling back the database."""
        # Create a migration file
        create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )

        # Migrate the database
        migrate_database(None, temp_migrations_dir, db)

        # Verify that the migration was applied
        assert db.table_exists("users")

        # Roll back the database
        rolled_back_migrations = rollback_database(1, temp_migrations_dir, db)

        # Verify that the migration was rolled back
        assert len(rolled_back_migrations) == 1
        assert rolled_back_migrations[0].version == 1
        assert not db.table_exists("users")

    def test_get_database_version(self, db, temp_migrations_dir):
        """Test getting the database version."""
        # Initially, should be 0
        assert get_database_version(temp_migrations_dir, db) == 0

        # Create and apply a migration
        create_test_migration_file(
            temp_migrations_dir, 1, "create_users",
            "CREATE TABLE users (id INTEGER PRIMARY KEY);",
            "DROP TABLE users;"
        )
        migrate_database(None, temp_migrations_dir, db)

        # Version should now be 1
        assert get_database_version(temp_migrations_dir, db) == 1

    def test_create_migration(self, temp_migrations_dir, db):
        """Test creating a new migration."""
        # Create a migration
        up_sql = "CREATE TABLE test_table (id INTEGER PRIMARY KEY);"
        down_sql = "DROP TABLE test_table;"
        migration_info = create_migration(
            "test_migration", up_sql, down_sql, temp_migrations_dir, db
        )

        # Verify that the migration was created
        assert migration_info.version == 1
        assert migration_info.name == "test_migration"

        # Verify that the migration files were created
        up_file = Path(temp_migrations_dir) / "0001_test_migration.sql"
        down_file = Path(temp_migrations_dir) / "0001_test_migration.down.sql"
        assert up_file.exists()
        assert down_file.exists()
