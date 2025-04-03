#!/usr/bin/env python3
from bot.db.migrations import (
    MigrationInfo, MigrationManager, initialise_migration_manager,
    migrate_database, rollback_database, get_database_version, create_migration
)
from bot.db.connection import Database, initialise_db_connection, get_db
from bot.core.config import ConfigManager, get_config
import argparse
import os
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Union, cast
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def format_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_migration_info(migration: MigrationInfo, current_version: int) -> str:
    status = "Applied" if migration.applied else "Pending"
    current = " (current)" if migration.version == current_version else ""
    applied_at = f" on {format_datetime(migration.applied_at)}" if migration.applied_at else ""
    return f"v{migration.version:04d} - {migration.name} [{status}{current}{applied_at}]"


def show_migration_status(migrations_dir: Union[str, Path]) -> None:
    print("Migration Status:")
    print("================")
    try:
        db = get_db()
        manager = initialise_migration_manager(migrations_dir, db)
        current_version = manager.get_current_version()
        available_migrations = manager.get_available_migrations()
        if not available_migrations:
            print("No migrations found.")
            return
        print(f"Current version: {current_version}")
        print()
        print("Migrations:")
        for version in sorted(available_migrations.keys()):
            migration = available_migrations[version]
            print(f"  {format_migration_info(migration, current_version)}")
    except Exception as e:
        print(f"Error showing migration status: {str(e)}")
        sys.exit(1)


def apply_migrations(migrations_dir: Union[str, Path], target_version: Optional[int] = None) -> None:
    print("Applying migrations:")
    print("===================")
    try:
        db = get_db()
        manager = initialise_migration_manager(migrations_dir, db)
        current_version = manager.get_current_version()
        print(f"Current version: {current_version}")
        if target_version is not None:
            print(f"Migrating to version: {target_version}")
            applied, rolled_back = manager.migrate_to_version(target_version)
            if applied:
                print("\nApplied migrations:")
                for migration in applied:
                    print(f"  v{migration.version:04d} - {migration.name}")
            if rolled_back:
                print("\nRolled back migrations:")
                for migration in rolled_back:
                    print(f"  v{migration.version:04d} - {migration.name}")
        else:
            print("Applying all pending migrations")
            applied = manager.migrate()
            if applied:
                print("\nApplied migrations:")
                for migration in applied:
                    print(f"  v{migration.version:04d} - {migration.name}")
            else:
                print("\nNo migrations to apply.")
        new_version = manager.get_current_version()
        print(f"\nNew version: {new_version}")
    except Exception as e:
        print(f"Error applying migrations: {str(e)}")
        sys.exit(1)


def rollback_migrations(migrations_dir: Union[str, Path], steps: int = 1) -> None:
    print("Rolling back migrations:")
    print("=======================")
    try:
        db = get_db()
        manager = initialise_migration_manager(migrations_dir, db)
        current_version = manager.get_current_version()
        print(f"Current version: {current_version}")
        if current_version == 0:
            print("No migrations to roll back.")
            return
        print(f"Rolling back {steps} migration(s)")
        rolled_back = manager.rollback(steps)
        if rolled_back:
            print("\nRolled back migrations:")
            for migration in rolled_back:
                print(f"  v{migration.version:04d} - {migration.name}")
        else:
            print("\nNo migrations were rolled back.")
        new_version = manager.get_current_version()
        print(f"\nNew version: {new_version}")
    except Exception as e:
        print(f"Error rolling back migrations: {str(e)}")
        sys.exit(1)


def create_new_migration(migrations_dir: Union[str, Path], name: str) -> None:
    print("Creating new migration:")
    print("=====================")
    try:
        db = get_db()
        manager = initialise_migration_manager(migrations_dir, db)
        up_sql = textwrap.dedent("""
            -- Migration: {name}
            -- Created: {datetime}
            
            -- Write your migration SQL here
            -- CREATE TABLE example (
            --     id INTEGER PRIMARY KEY,
            --     name TEXT NOT NULL
            -- );
        """).format(
            name=name,
            datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ).strip()
        down_sql = textwrap.dedent("""
            -- Migration rollback: {name}
            -- Created: {datetime}
            
            -- Write your rollback SQL here
            -- DROP TABLE example;
        """).format(
            name=name,
            datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ).strip()
        migration = manager.create_migration(name, up_sql, down_sql)
        print(
            f"Created migration: v{migration.version:04d} - {migration.name}")
        print(f"Up SQL file: {os.path.basename(migration.file_path)}")
        print(
            f"Down SQL file: {os.path.basename(migration.file_path).replace('.sql', '.down.sql')}")
        print("\nEdit these files to define your migration.")

    except Exception as e:
        print(f"Error creating migration: {str(e)}")
        sys.exit(1)


def init_database_connection(env_file: Optional[str] = None) -> None:
    try:
        config = get_config()
        if env_file:
            config.load(env_file)
        else:
            config.load()
        db_path = config.get("db_path")
        if not db_path:
            print("Error: Database path not specified in configuration.")
            sys.exit(1)
        initialise_db_connection(db_path)
    except Exception as e:
        print(f"Error initialising database connection: {str(e)}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Database migration script",
        formatter_class=argparse.RawTextHelpFormatter
    )
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--up", action="store_true",
        help="Apply pending migrations (default)"
    )
    action_group.add_argument(
        "--down", type=int, nargs="?", const=1, metavar="STEPS",
        help="Roll back migrations (default: 1)"
    )
    action_group.add_argument(
        "--to", type=int, metavar="VERSION",
        help="Migrate to a specific version"
    )
    action_group.add_argument(
        "--create", type=str, metavar="NAME",
        help="Create a new migration with the given name"
    )
    action_group.add_argument(
        "--status", action="store_true",
        help="Show migration status"
    )
    parser.add_argument(
        "--env", type=str, metavar="ENV_FILE",
        help="Path to environment file (default: .env)"
    )
    parser.add_argument(
        "--migrations-dir", type=str, metavar="DIR",
        help="Path to migrations directory (default: migrations)"
    )
    args = parser.parse_args()
    migrations_dir = args.migrations_dir
    if not migrations_dir:
        try:
            from bot.core.constants import PROJECT_ROOT
            migrations_dir = os.path.join(PROJECT_ROOT, "migrations")
        except ImportError:
            migrations_dir = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), "migrations")
    os.makedirs(migrations_dir, exist_ok=True)
    init_database_connection(args.env)
    if args.create:
        create_new_migration(migrations_dir, args.create)
    elif args.down is not None:
        rollback_migrations(migrations_dir, args.down)
    elif args.to is not None:
        apply_migrations(migrations_dir, args.to)
    elif args.status:
        show_migration_status(migrations_dir)
    else:
        apply_migrations(migrations_dir)


if __name__ == "__main__":
    main()
