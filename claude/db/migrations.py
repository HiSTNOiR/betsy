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
logger = logging.getLogger(__name__)


class MigrationError(DatabaseError):
    pass


class MigrationVersionError(MigrationError):
    pass


class MigrationFileError(MigrationError):
    pass


class MigrationApplyError(MigrationError):
    pass


class MigrationRollbackError(MigrationError):
    pass


@dataclass
class MigrationInfo:
    version: int
    name: str
    file_path: str
    applied: bool = False
    applied_at: Optional[datetime] = None


class Migration:
    def __init__(self, db: Database):
        self.db = db
        self.version = 0
        self.name = "base_migration"

    def up(self) -> None:
        raise NotImplementedError("Subclasses must implement up()")

    def down(self) -> None:
        raise NotImplementedError("Subclasses must implement down()")


class SQLMigration(Migration):
    def __init__(self, db: Database, up_sql: str, down_sql: Optional[str] = None):
        super().__init__(db)
        self._up_sql = up_sql
        self._down_sql = down_sql

    def up(self) -> None:
        try:
            statements = self._split_sql_script(self._up_sql)
            for statement in statements:
                if statement.strip():
                    self.db.execute(statement)
        except Exception as e:
            error_msg = f"Error applying migration: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise MigrationApplyError(error_msg) from e

    def down(self) -> None:
        if not self._down_sql:
            error_msg = "No rollback SQL provided for this migration"
            logger.error(error_msg)
            raise MigrationRollbackError(error_msg)
        try:
            statements = self._split_sql_script(self._down_sql)
            for statement in statements:
                if statement.strip():
                    self.db.execute(statement)
        except Exception as e:
            error_msg = f"Error rolling back migration: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise MigrationRollbackError(error_msg) from e

    def _split_sql_script(self, script: str) -> List[str]:
        statements = []
        current_statement = []
        for line in script.splitlines():
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('--'):
                continue
            current_statement.append(line)
            if stripped_line.endswith(';'):
                statements.append('\n'.join(current_statement))
                current_statement = []
        if current_statement:
            statements.append('\n'.join(current_statement))
        return statements


class MigrationManager:
    MIGRATIONS_TABLE = "migrations"
    MIGRATION_FILENAME_PATTERN = re.compile(r"^(\d{4})_([a-zA-Z0-9_]+)\.sql$")

    def __init__(self, db: Database, migrations_dir: Union[str, Path], create_table: bool = True):
        self._db = db
        self._migrations_dir = Path(migrations_dir)
        if not self._migrations_dir.exists() or not self._migrations_dir.is_dir():
            error_msg = f"Migrations directory not found: {self._migrations_dir}"
            logger.error(error_msg)
            raise MigrationError(error_msg)
        if create_table:
            try:
                self._create_migrations_table()
            except Exception as e:
                error_msg = f"Failed to create migrations table: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise MigrationError(error_msg) from e

    def _create_migrations_table(self) -> None:
        if self._db.table_exists(self.MIGRATIONS_TABLE):
            logger.debug(
                f"Migrations table '{self.MIGRATIONS_TABLE}' already exists")
            return

        logger.info(f"Creating migrations table '{self.MIGRATIONS_TABLE}'")
        query = f"""
        CREATE TABLE {self.MIGRATIONS_TABLE} (
            version INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            applied_at TIMESTAMP NOT NULL
        )
        """
        self._db.execute(query)

    def get_applied_migrations(self) -> Dict[int, MigrationInfo]:
        if not self._db.table_exists(self.MIGRATIONS_TABLE):
            return {}
        query = f"SELECT version, name, applied_at FROM {self.MIGRATIONS_TABLE} ORDER BY version"
        rows = self._db.fetchall(query)
        migrations = {}
        for row in rows:
            version = row["version"]
            name = row["name"]
            applied_at_str = row["applied_at"]
            try:
                applied_at = datetime.fromisoformat(applied_at_str)
            except ValueError:
                applied_at = datetime.strptime(
                    applied_at_str, "%Y-%m-%d %H:%M:%S")
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
        migrations = {}
        applied_migrations = self.get_applied_migrations()
        try:
            for file_path in sorted(self._migrations_dir.glob("*.sql")):
                match = self.MIGRATION_FILENAME_PATTERN.match(file_path.name)
                if not match:
                    logger.warning(
                        f"Ignoring file with invalid migration name: {file_path.name}")
                    continue
                version = int(match.group(1))
                name = match.group(2)
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
        available_migrations = self.get_available_migrations()
        pending_migrations = [
            migration for migration in available_migrations.values()
            if not migration.applied
        ]
        return sorted(pending_migrations, key=lambda m: m.version)

    def get_migration(self, version: int) -> Optional[MigrationInfo]:
        available_migrations = self.get_available_migrations()
        return available_migrations.get(version)

    def record_migration(self, version: int, name: str) -> None:
        applied_at = datetime.now().isoformat()
        query = f"INSERT INTO {self.MIGRATIONS_TABLE} (version, name, applied_at) VALUES (?, ?, ?)"
        self._db.execute(query, (version, name, applied_at))
        logger.info(f"Recorded migration: v{version} ({name})")

    def remove_migration_record(self, version: int) -> None:
        query = f"DELETE FROM {self.MIGRATIONS_TABLE} WHERE version = ?"
        self._db.execute(query, (version,))
        logger.info(f"Removed migration record: v{version}")

    def apply_migration(self, migration_info: MigrationInfo) -> None:
        version = migration_info.version
        name = migration_info.name
        file_path = migration_info.file_path
        logger.info(f"Applying migration: v{version} ({name})")
        try:
            with open(file_path, 'r') as f:
                up_sql = f.read()
            down_file = Path(file_path).with_name(
                f"{version:04d}_{name}.down.sql")
            down_sql = None
            if down_file.exists():
                with open(down_file, 'r') as f:
                    down_sql = f.read()
            migration = SQLMigration(self._db, up_sql, down_sql)
            migration.version = version
            migration.name = name
            with self._db.transaction():
                migration.up()
                self.record_migration(version, name)
            logger.info(f"Successfully applied migration: v{version} ({name})")
        except Exception as e:
            error_msg = f"Failed to apply migration v{version} ({name}): {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise MigrationApplyError(error_msg) from e

    def rollback_migration(self, migration_info: MigrationInfo) -> None:
        version = migration_info.version
        name = migration_info.name
        file_path = migration_info.file_path
        logger.info(f"Rolling back migration: v{version} ({name})")
        try:
            down_file = Path(file_path).with_name(
                f"{version:04d}_{name}.down.sql")
            if not down_file.exists():
                error_msg = f"No rollback script found for migration v{version} ({name})"
                logger.error(error_msg)
                raise MigrationRollbackError(error_msg)
            with open(file_path, 'r') as f:
                up_sql = f.read()
            with open(down_file, 'r') as f:
                down_sql = f.read()
            migration = SQLMigration(self._db, up_sql, down_sql)
            migration.version = version
            migration.name = name
            with self._db.transaction():
                migration.down()
                self.remove_migration_record(version)
            logger.info(
                f"Successfully rolled back migration: v{version} ({name})")
        except Exception as e:
            error_msg = f"Failed to roll back migration v{version} ({name}): {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise MigrationRollbackError(error_msg) from e

    def migrate(self, target_version: Optional[int] = None) -> List[MigrationInfo]:
        pending_migrations = self.get_pending_migrations()
        if not pending_migrations:
            logger.info("No pending migrations to apply")
            return []
        if target_version is not None:
            pending_migrations = [
                m for m in pending_migrations if m.version <= target_version]
            if not pending_migrations:
                logger.info(
                    f"No pending migrations up to version {target_version}")
                return []
        applied_migrations = []
        for migration in pending_migrations:
            try:
                self.apply_migration(migration)
                applied_migrations.append(migration)
            except Exception as e:
                logger.error(
                    f"Error applying migration v{migration.version} ({migration.name}): {str(e)}",
                    exc_info=True
                )
                if isinstance(e, TransactionError):
                    logger.error(
                        "Transaction error, stopping migration process")
                    break
        logger.info(f"Applied {len(applied_migrations)} migrations")
        return applied_migrations

    def rollback(self, steps: int = 1) -> List[MigrationInfo]:
        applied_migrations = self.get_applied_migrations()
        if not applied_migrations:
            logger.info("No migrations to roll back")
            return []
        migrations_to_rollback = sorted(
            applied_migrations.values(),
            key=lambda m: m.version,
            reverse=True
        )[:steps]
        if not migrations_to_rollback:
            logger.info("No migrations to roll back")
            return []
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
        current_version = self.get_current_version()
        if current_version == version:
            logger.info(f"Already at version {version}")
            return [], []
        if current_version < version:
            applied = self.migrate(target_version=version)
            return applied, []
        else:
            applied_migrations = self.get_applied_migrations()
            migrations_to_rollback = [
                m for m in applied_migrations.values()
                if m.version > version
            ]
            migrations_to_rollback.sort(key=lambda m: m.version, reverse=True)
            rolled_back = []
            for migration in migrations_to_rollback:
                try:
                    self.rollback_migration(migration)
                    rolled_back.append(migration)
                except Exception as e:
                    logger.error(
                        f"Error rolling back migration v{migration.version} ({migration.name}): {str(e)}",
                        exc_info=True
                    )
                    break
            return [], rolled_back

    def get_current_version(self) -> int:
        applied_migrations = self.get_applied_migrations()
        if not applied_migrations:
            return 0
        return max(applied_migrations.keys())

    def create_migration(self, name: str, up_sql: str, down_sql: Optional[str] = None) -> MigrationInfo:
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
        available_migrations = self.get_available_migrations()
        if available_migrations:
            next_version = max(available_migrations.keys()) + 1
        else:
            next_version = 1
        file_name = f"{next_version:04d}_{name}.sql"
        file_path = self._migrations_dir / file_name
        down_file_path = None
        if down_sql:
            down_file_name = f"{next_version:04d}_{name}.down.sql"
            down_file_path = self._migrations_dir / down_file_name
        try:
            os.makedirs(self._migrations_dir, exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(up_sql)
            if down_sql and down_file_path:
                with open(down_file_path, 'w') as f:
                    f.write(down_sql)
            logger.info(f"Created migration file: {file_name}")
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


def initialise_migration_manager(
    migrations_dir: Optional[Union[str, Path]] = None,
    db: Optional[Database] = None
) -> MigrationManager:
    try:
        database = db or get_db()
        if migrations_dir is None:
            try:
                from bot.core.constants import PROJECT_ROOT
                migrations_dir = Path(PROJECT_ROOT) / "migrations"
            except ImportError:
                module_dir = Path(__file__).parent
                migrations_dir = module_dir / "migrations"
        os.makedirs(migrations_dir, exist_ok=True)
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
    manager = initialise_migration_manager(migrations_dir, db)
    return manager.migrate(target_version)


def rollback_database(
    steps: int = 1,
    migrations_dir: Optional[Union[str, Path]] = None,
    db: Optional[Database] = None
) -> List[MigrationInfo]:
    manager = initialise_migration_manager(migrations_dir, db)
    return manager.rollback(steps)


def get_database_version(
    migrations_dir: Optional[Union[str, Path]] = None,
    db: Optional[Database] = None
) -> int:
    manager = initialise_migration_manager(migrations_dir, db)
    return manager.get_current_version()


def create_migration(
    name: str,
    up_sql: str,
    down_sql: Optional[str] = None,
    migrations_dir: Optional[Union[str, Path]] = None,
    db: Optional[Database] = None
) -> MigrationInfo:
    manager = initialise_migration_manager(migrations_dir, db)
    return manager.create_migration(name, up_sql, down_sql)
