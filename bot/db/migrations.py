"""
Database migration system for the bot.

This module provides functionality for managing database schema migrations,
including version tracking, applying migrations, and rollbacks.
"""

import importlib
import logging
import os
import re
import sqlite3
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union, cast

from bot.db.connection import Database, DatabaseError, QueryError, TransactionError, get_db

# Set up logger for this module
logger = logging.getLogger(__name__)


class MigrationError(DatabaseError):
    """Exception raised for migration-related errors."""
    pass


class MigrationVersionError(MigrationError):
    """Exception raised for migration version errors."""
    pass


class MigrationFileError(MigrationError):
    """Exception raised for migration file errors."""
    pass


class MigrationApplyError(MigrationError):
    """Exception raised when a migration cannot be applied."""
    pass


class MigrationRollbackError(MigrationError):
    """Exception raised when a migration cannot be rolled back."""
    pass


@dataclass
class MigrationInfo:
    """Information about a migration."""
    version: int
    name: str
    file_path: str
    applied: bool = False
    applied_at: Optional[datetime] = None


class Migration:
    """
    Base class for database migrations.

    All migrations should inherit from this class and implement the up() and down() methods.
    """

    def __init__(self, db: Database):
        """
        Initialize the migration.

        Args:
            db (Database): Database connection.
        """
        self.db = db
        self.version = 0
        self.name = "base_migration"

    def up(self) -> None:
        """
        Apply the migration.

        This method should be implemented by subclasses to make the necessary changes
        to upgrade the database schema.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement up()")

    def down(self) -> None:
        """
        Rollback the migration.

        This method should be implemented by subclasses to make the necessary changes
        to downgrade the database schema.

        Raises:
            NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError("Subclasses must implement down()")


class SQLMigration(Migration):
    """
    Migration that executes SQL scripts for up and down operations.

    This class simplifies creating migrations by allowing SQL files to be used
    instead of Python code.
    """

    def __init__(self, db: Database, up_sql: str, down_sql: Optional[str] = None):
        """
        Initialize the SQL migration.

        Args:
            db (Database): Database connection.
            up_sql (str): SQL script for applying the migration.
            down_sql (Optional[str]): SQL script for rolling back the migration.
                If None, the migration cannot be rolled back.
        """
        super().__init__(db)
        self._up_sql = up_sql
        self._down_sql = down_sql

    def up(self) -> None:
        """
        Apply the migration using the provided SQL script.

        Raises:
            MigrationApplyError: If the SQL script cannot be executed.
        """
        try:
            # Split script into individual statements
            statements = self._split_sql_script(self._up_sql)

            # Execute each statement
            for statement in statements:
                if statement.strip():
                    self.db.execute(statement)
        except Exception as e:
            error_msg = f"Error applying migration: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise MigrationApplyError(error_msg) from e

    def down(self) -> None:
        """
        Rollback the migration using the provided SQL script.

        Raises:
            MigrationRollbackError: If the SQL script cannot be executed or is not provided.
        """
        if not self._down_sql:
            error_msg = "No rollback SQL provided for this migration"
            logger.error(error_msg)
            raise MigrationRollbackError(error_msg)

        try:
            # Split script into individual statements
            statements = self._split_sql_script(self._down_sql)

            # Execute each statement
            for statement in statements:
                if statement.strip():
                    self.db.execute(statement)
        except Exception as e:
            error_msg = f"Error rolling back migration: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise MigrationRollbackError(error_msg) from e

    def _split_sql_script(self, script: str) -> List[str]:
        """
        Split a SQL script into individual statements.

        Args:
            script (str): SQL script.

        Returns:
            List[str]: List of SQL statements.
        """
        # Simple splitting by semicolon - this works for basic SQL scripts
        # but might not handle all edge cases (like semicolons in strings or triggers)
        statements = []
        current_statement = []

        for line in script.splitlines():
            # Skip empty lines and comments
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('--'):
                continue

            current_statement.append(line)

            if stripped_line.endswith(';'):
                statements.append('\n'.join(current_statement))
                current_statement = []

        # Add any remaining statement
        if current_statement:
            statements.append('\n'.join(current_statement))

        return statements


class MigrationManager:
    """
    Manages database migrations.

    This class provides functionality for applying and rolling back migrations,
    as well as tracking which migrations have been applied.
    """

    # Table name for storing migration information
    MIGRATIONS_TABLE = "migrations"

    # Migration filename pattern: NNNN_name.sql
    MIGRATION_FILENAME_PATTERN = re.compile(r"^(\d{4})_([a-zA-Z0-9_]+)\.sql$")

    def __init__(self, db: Database, migrations_dir: Union[str, Path], create_table: bool = True):
        """
        Initialize the migration manager.

        Args:
            db (Database): Database connection.
            migrations_dir (Union[str, Path]): Directory containing migration files.
            create_table (bool): Whether to create the migrations table if it doesn't exist.

        Raises:
            MigrationError: If the migrations directory doesn't exist or the migrations table
                cannot be created.
        """
        self._db = db
        self._migrations_dir = Path(migrations_dir)

        # Ensure migrations directory exists
        if not self._migrations_dir.exists() or not self._migrations_dir.is_dir():
            error_msg = f"Migrations directory not found: {self._migrations_dir}"
            logger.error(error_msg)
            raise MigrationError(error_msg)

        # Create migrations table if requested
        if create_table:
            try:
                self._create_migrations_table()
            except Exception as e:
                error_msg = f"Failed to create migrations table: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise MigrationError(error_msg) from e

    def _create_migrations_table(self) -> None:
        """
        Create the migrations table if it doesn't exist.

        Raises:
            QueryError: If the table cannot be created.
        """
        # Check if table exists
        if self._db.table_exists(self.MIGRATIONS_TABLE):
            logger.debug(
                f"Migrations table '{self.MIGRATIONS_TABLE}' already exists")
            return

        logger.info(f"Creating migrations table '{self.MIGRATIONS_TABLE}'")

        # Create the table
        query = f"""
        CREATE TABLE {self.MIGRATIONS_TABLE} (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TIMESTAMP NOT NULL
        )
        """
        self._db.execute(query)

    def get_applied_migrations(self) -> Dict[int, MigrationInfo]:
        """
        Get all applied migrations.

        Returns:
            Dict[int, MigrationInfo]: Dictionary mapping version numbers to migration info.

        Raises:
            QueryError: If the migrations cannot be retrieved.
        """
        # Check if table exists
        if not self._db.table_exists(self.MIGRATIONS_TABLE):
            return {}

        # Get applied migrations
        query = f"SELECT version, name, applied_at FROM {self.MIGRATIONS_TABLE} ORDER BY version"
        rows = self._db.fetchall(query)

        # Convert to MigrationInfo objects
        migrations = {}
        for row in rows:
            version = row["version"]
            name = row["name"]
            applied_at_str = row["applied_at"]

            try:
                applied_at = datetime.fromisoformat(applied_at_str)
            except ValueError:
                # Fall back to legacy parsing if needed
                applied_at = datetime.strptime(
                    applied_at_str, "%Y-%m-%d %H:%M:%S")

            # Create a placeholder file path - we don't know the actual path
            file_path = str(self._migrations_dir / f"{version:04d}_{name}.sql")

            migrations[version] = MigrationInfo(
                version=version,
                name=name,
                file_path=file_path,
                applied=True,
                applied_at=applied_at
            )

        return migrations

    def get_available_migrations(self) -> Dict[int, MigrationInfo]:
        """
        Get all available migrations from the migrations directory.

        Returns:
            Dict[int, MigrationInfo]: Dictionary mapping version numbers to migration info.

        Raises:
            MigrationFileError: If migration files cannot be processed.
        """
        migrations = {}

        # Get applied migrations to check which are already applied
        applied_migrations = self.get_applied_migrations()

        try:
            # Process each migration file
            for file_path in sorted(self._migrations_dir.glob("*.sql")):
                match = self.MIGRATION_FILENAME_PATTERN.match(file_path.name)
                if not match:
                    logger.warning(
                        f"Ignoring file with invalid migration name: {file_path.name}")
                    continue

                version = int(match.group(1))
                name = match.group(2)

                # Check if already applied
                applied = version in applied_migrations
                applied_at = applied_migrations[version].applied_at if applied else None

                migrations[version] = MigrationInfo(
                    version=version,
                    name=name,
                    file_path=str(file_path),
                    applied=applied,
                    applied_at=applied_at
                )
        except Exception as e:
            error_msg = f"Error processing migration files: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise MigrationFileError(error_msg) from e

        return migrations

    def get_pending_migrations(self) -> List[MigrationInfo]:
        """
        Get migrations that have not been applied yet.

        Returns:
            List[MigrationInfo]: List of pending migrations, sorted by version.

        Raises:
            MigrationFileError: If migration files cannot be processed.
        """
        # Get all available migrations
        available_migrations = self.get_available_migrations()

        # Filter out applied migrations
        pending_migrations = [
            migration for migration in available_migrations.values()
            if not migration.applied
        ]

        # Sort by version
        return sorted(pending_migrations, key=lambda m: m.version)

    def get_migration(self, version: int) -> Optional[MigrationInfo]:
        """
        Get information about a specific migration.

        Args:
            version (int): Migration version.

        Returns:
            Optional[MigrationInfo]: Migration information, or None if not found.

        Raises:
            MigrationFileError: If migration files cannot be processed.
        """
        # Get all available migrations
        available_migrations = self.get_available_migrations()

        # Return the requested migration, if available
        return available_migrations.get(version)

    def record_migration(self, version: int, name: str) -> None:
        """
        Record that a migration has been applied.

        Args:
            version (int): Migration version.
            name (str): Migration name.

        Raises:
            QueryError: If the migration cannot be recorded.
        """
        # Get current time
        applied_at = datetime.now().isoformat()

        # Insert migration record
        query = f"INSERT INTO {self.MIGRATIONS_TABLE} (version, name, applied_at) VALUES (?, ?, ?)"
        self._db.execute(query, (version, name, applied_at))

        logger.info(f"Recorded migration: v{version} ({name})")

    def remove_migration_record(self, version: int) -> None:
        """
        Remove a migration record.

        Args:
            version (int): Migration version.

        Raises:
            QueryError: If the migration record cannot be removed.
        """
        # Delete migration record
        query = f"DELETE FROM {self.MIGRATIONS_TABLE} WHERE version = ?"
        self._db.execute(query, (version,))

        logger.info(f"Removed migration record: v{version}")

    def apply_migration(self, migration_info: MigrationInfo) -> None:
        """
        Apply a single migration.

        Args:
            migration_info (MigrationInfo): Migration to apply.

        Raises:
            MigrationApplyError: If the migration cannot be applied.
        """
        version = migration_info.version
        name = migration_info.name
        file_path = migration_info.file_path

        logger.info(f"Applying migration: v{version} ({name})")

        try:
            # Read migration file
            with open(file_path, 'r') as f:
                up_sql = f.read()

            # Check for a corresponding down file
            down_file = Path(file_path).with_name(
                f"{version:04d}_{name}.down.sql")
            down_sql = None
            if down_file.exists():
                with open(down_file, 'r') as f:
                    down_sql = f.read()

            # Create migration
            migration = SQLMigration(self._db, up_sql, down_sql)
            migration.version = version
            migration.name = name

            # Apply migration within a transaction
            with self._db.transaction():
                # Apply the migration
                migration.up()

                # Record the migration
                self.record_migration(version, name)

            logger.info(f"Successfully applied migration: v{version} ({name})")
        except Exception as e:
            error_msg = f"Failed to apply migration v{version} ({name}): {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise MigrationApplyError(error_msg) from e

    def rollback_migration(self, migration_info: MigrationInfo) -> None:
        """
        Rollback a single migration.

        Args:
            migration_info (MigrationInfo): Migration to roll back.

        Raises:
            MigrationRollbackError: If the migration cannot be rolled back.
        """
        version = migration_info.version
        name = migration_info.name
        file_path = migration_info.file_path

        logger.info(f"Rolling back migration: v{version} ({name})")

        try:
            # Check for a down file
            down_file = Path(file_path).with_name(
                f"{version:04d}_{name}.down.sql")
            if not down_file.exists():
                error_msg = f"No rollback script found for migration v{version} ({name})"
                logger.error(error_msg)
                raise MigrationRollbackError(error_msg)

            # Read migration files
            with open(file_path, 'r') as f:
                up_sql = f.read()

            with open(down_file, 'r') as f:
                down_sql = f.read()

            # Create migration
            migration = SQLMigration(self._db, up_sql, down_sql)
            migration.version = version
            migration.name = name

            # Roll back migration within a transaction
            with self._db.transaction():
                # Roll back the migration
                migration.down()

                # Remove the migration record
                self.remove_migration_record(version)

            logger.info(
                f"Successfully rolled back migration: v{version} ({name})")
        except Exception as e:
            error_msg = f"Failed to roll back migration v{version} ({name}): {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise MigrationRollbackError(error_msg) from e

    def migrate(self, target_version: Optional[int] = None) -> List[MigrationInfo]:
        """
        Apply pending migrations.

        Args:
            target_version (Optional[int]): Target version to migrate to.
                If None, applies all pending migrations.

        Returns:
            List[MigrationInfo]: List of applied migrations.

        Raises:
            MigrationApplyError: If a migration cannot be applied.
        """
        # Get pending migrations
        pending_migrations = self.get_pending_migrations()

        if not pending_migrations:
            logger.info("No pending migrations to apply")
            return []

        # Filter migrations based on target version
        if target_version is not None:
            pending_migrations = [
                m for m in pending_migrations if m.version <= target_version]
            if not pending_migrations:
                logger.info(
                    f"No pending migrations up to version {target_version}")
                return []

        # Apply migrations
        applied_migrations = []
        for migration in pending_migrations:
            try:
                self.apply_migration(migration)
                applied_migrations.append(migration)
            except Exception as e:
                # Log the error but don't re-raise, so we can continue applying other migrations
                logger.error(
                    f"Error applying migration v{migration.version} ({migration.name}): {str(e)}",
                    exc_info=True
                )
                # If we're in a transaction, stop applying migrations
                if isinstance(e, TransactionError):
                    logger.error(
                        "Transaction error, stopping migration process")
                    break

        logger.info(f"Applied {len(applied_migrations)} migrations")
        return applied_migrations

    def rollback(self, steps: int = 1) -> List[MigrationInfo]:
        """
        Rollback applied migrations.

        Args:
            steps (int): Number of migrations to roll back.

        Returns:
            List[MigrationInfo]: List of rolled back migrations.

        Raises:
            MigrationRollbackError: If a migration cannot be rolled back.
        """
        # Get applied migrations
        applied_migrations = self.get_applied_migrations()

        if not applied_migrations:
            logger.info("No migrations to roll back")
            return []

        # Sort migrations by version in descending order
        migrations_to_rollback = sorted(
            applied_migrations.values(),
            key=lambda m: m.version,
            reverse=True
        )[:steps]

        if not migrations_to_rollback:
            logger.info("No migrations to roll back")
            return []

        # Roll back migrations
        rolled_back_migrations = []
        for migration in migrations_to_rollback:
            try:
                self.rollback_migration(migration)
                rolled_back_migrations.append(migration)
            except Exception as e:
                # Log the error and stop rolling back
                logger.error(
                    f"Error rolling back migration v{migration.version} ({migration.name}): {str(e)}",
                    exc_info=True
                )
                break

        logger.info(f"Rolled back {len(rolled_back_migrations)} migrations")
        return rolled_back_migrations

    def migrate_to_version(self, version: int) -> Tuple[List[MigrationInfo], List[MigrationInfo]]:
        """
        Migrate to a specific version.

        This may involve applying or rolling back migrations.

        Args:
            version (int): Target version.

        Returns:
            Tuple[List[MigrationInfo], List[MigrationInfo]]: 
                Lists of (applied_migrations, rolled_back_migrations).

        Raises:
            MigrationError: If migrations cannot be applied or rolled back.
        """
        # Get current version
        current_version = self.get_current_version()

        # If we're already at the target version, do nothing
        if current_version == version:
            logger.info(f"Already at version {version}")
            return [], []

        # If we need to go forward
        if current_version < version:
            applied = self.migrate(target_version=version)
            return applied, []

        # If we need to go backward
        else:
            # Get all applied migrations
            applied_migrations = self.get_applied_migrations()

            # Filter migrations that need to be rolled back
            migrations_to_rollback = [
                m for m in applied_migrations.values()
                if m.version > version
            ]

            # Sort in descending order
            migrations_to_rollback.sort(key=lambda m: m.version, reverse=True)

            # Roll back migrations
            rolled_back = []
            for migration in migrations_to_rollback:
                try:
                    self.rollback_migration(migration)
                    rolled_back.append(migration)
                except Exception as e:
                    # Log the error and stop rolling back
                    logger.error(
                        f"Error rolling back migration v{migration.version} ({migration.name}): {str(e)}",
                        exc_info=True
                    )
                    break

            return [], rolled_back

    def get_current_version(self) -> int:
        """
        Get the current migration version.

        Returns:
            int: Current version, or 0 if no migrations have been applied.
        """
        # Get applied migrations
        applied_migrations = self.get_applied_migrations()

        if not applied_migrations:
            return 0

        # Return the highest version
        return max(applied_migrations.keys())

    def create_migration(self, name: str, up_sql: str, down_sql: Optional[str] = None) -> MigrationInfo:
        """
        Create a new migration file.

        Args:
            name (str): Migration name.
            up_sql (str): SQL for applying the migration.
            down_sql (Optional[str]): SQL for rolling back the migration.

        Returns:
            MigrationInfo: Information about the created migration.

        Raises:
            MigrationFileError: If the migration file cannot be created.
        """
        # Sanitise the name
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())

        # Get the next version number
        available_migrations = self.get_available_migrations()
        if available_migrations:
            next_version = max(available_migrations.keys()) + 1
        else:
            next_version = 1

        # Create file names
        file_name = f"{next_version:04d}_{name}.sql"
        file_path = self._migrations_dir / file_name

        down_file_path = None
        if down_sql:
            down_file_name = f"{next_version:04d}_{name}.down.sql"
            down_file_path = self._migrations_dir / down_file_name

        try:
            # Create migration directory if it doesn't exist
            os.makedirs(self._migrations_dir, exist_ok=True)

            # Write the up SQL file
            with open(file_path, 'w') as f:
                f.write(up_sql)

            # Write the down SQL file if provided
            if down_sql and down_file_path:
                with open(down_file_path, 'w') as f:
                    f.write(down_sql)

            logger.info(f"Created migration file: {file_name}")

            # Return information about the created migration
            return MigrationInfo(
                version=next_version,
                name=name,
                file_path=str(file_path),
                applied=False
            )
        except Exception as e:
            error_msg = f"Failed to create migration file: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise MigrationFileError(error_msg) from e


# Helper functions for using the migration manager

def initialise_migration_manager(
    migrations_dir: Optional[Union[str, Path]] = None,
    db: Optional[Database] = None
) -> MigrationManager:
    """
    Initialize the migration manager.

    Args:
        migrations_dir (Optional[Union[str, Path]]): Directory containing migration files.
            If None, uses the default directory.
        db (Optional[Database]): Database connection.
            If None, uses the default connection.

    Returns:
        MigrationManager: Migration manager instance.

    Raises:
        MigrationError: If the migration manager cannot be initialized.
    """
    try:
        # Use provided database or get default
        database = db or get_db()

        # Use provided migrations directory or get default
        if migrations_dir is None:
            # Try to get the migrations directory from the project root
            try:
                from bot.core.constants import PROJECT_ROOT
                migrations_dir = Path(PROJECT_ROOT) / "migrations"
            except ImportError:
                # Fall back to a directory relative to the current file
                module_dir = Path(__file__).parent
                migrations_dir = module_dir / "migrations"

        # Create migrations directory if it doesn't exist
        os.makedirs(migrations_dir, exist_ok=True)

        # Create and return migration manager
        return MigrationManager(database, migrations_dir)
    except Exception as e:
        error_msg = f"Failed to initialise migration manager: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise MigrationError(error_msg) from e


def migrate_database(
    target_version: Optional[int] = None,
    migrations_dir: Optional[Union[str, Path]] = None,
    db: Optional[Database] = None
) -> List[MigrationInfo]:
    """
    Apply pending database migrations.

    Args:
        target_version (Optional[int]): Target version to migrate to.
            If None, applies all pending migrations.
        migrations_dir (Optional[Union[str, Path]]): Directory containing migration files.
            If None, uses the default directory.
        db (Optional[Database]): Database connection.
            If None, uses the default connection.

    Returns:
        List[MigrationInfo]: List of applied migrations.

    Raises:
        MigrationError: If migrations cannot be applied.
    """
    # Initialize migration manager
    manager = initialise_migration_manager(migrations_dir, db)

    # Apply migrations
    return manager.migrate(target_version)


def rollback_database(
    steps: int = 1,
    migrations_dir: Optional[Union[str, Path]] = None,
    db: Optional[Database] = None
) -> List[MigrationInfo]:
    """
    Rollback applied database migrations.

    Args:
        steps (int): Number of migrations to roll back.
        migrations_dir (Optional[Union[str, Path]]): Directory containing migration files.
            If None, uses the default directory.
        db (Optional[Database]): Database connection.
            If None, uses the default connection.

    Returns:
        List[MigrationInfo]: List of rolled back migrations.

    Raises:
        MigrationError: If migrations cannot be rolled back.
    """
    # Initialize migration manager
    manager = initialise_migration_manager(migrations_dir, db)

    # Roll back migrations
    return manager.rollback(steps)


def get_database_version(
    migrations_dir: Optional[Union[str, Path]] = None,
    db: Optional[Database] = None
) -> int:
    """
    Get the current database version.

    Args:
        migrations_dir (Optional[Union[str, Path]]): Directory containing migration files.
            If None, uses the default directory.
        db (Optional[Database]): Database connection.
            If None, uses the default connection.

    Returns:
        int: Current database version.

    Raises:
        MigrationError: If the database version cannot be determined.
    """
    # Initialize migration manager
    manager = initialise_migration_manager(migrations_dir, db)

    # Get current version
    return manager.get_current_version()


def create_migration(
    name: str,
    up_sql: str,
    down_sql: Optional[str] = None,
    migrations_dir: Optional[Union[str, Path]] = None,
    db: Optional[Database] = None
) -> MigrationInfo:
    """
    Create a new database migration.

    Args:
        name (str): Migration name.
        up_sql (str): SQL for applying the migration.
        down_sql (Optional[str]): SQL for rolling back the migration.
        migrations_dir (Optional[Union[str, Path]]): Directory containing migration files.
            If None, uses the default directory.
        db (Optional[Database]): Database connection.
            If None, uses the default connection.

    Returns:
        MigrationInfo: Information about the created migration.

    Raises:
        MigrationError: If the migration cannot be created.
    """
    # Initialize migration manager
    manager = initialise_migration_manager(migrations_dir, db)

    # Create migration
    return manager.create_migration(name, up_sql, down_sql)
