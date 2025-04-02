"""
Database package for the bot.

This package provides database connectivity, schema management, and data access.
"""

from bot.db.connection import (
    Database,
    DatabaseError,
    ConnectionError,
    TransactionError,
    QueryError,
    initialise_db_connection,
    get_db,
    close_db_connection,
    db_transaction,
    with_db,
)

from bot.db.migrations import (
    Migration,
    SQLMigration,
    MigrationManager,
    MigrationInfo,
    MigrationError,
    MigrationVersionError,
    MigrationFileError,
    MigrationApplyError,
    MigrationRollbackError,
    initialise_migration_manager,
    migrate_database,
    rollback_database,
    get_database_version,
    create_migration,
)

__all__ = [
    # Connection classes
    "Database",

    # Connection exceptions
    "DatabaseError",
    "ConnectionError",
    "TransactionError",
    "QueryError",

    # Connection functions
    "initialise_db_connection",
    "get_db",
    "close_db_connection",
    "db_transaction",
    "with_db",

    # Migration classes
    "Migration",
    "SQLMigration",
    "MigrationManager",
    "MigrationInfo",

    # Migration exceptions
    "MigrationError",
    "MigrationVersionError",
    "MigrationFileError",
    "MigrationApplyError",
    "MigrationRollbackError",

    # Migration functions
    "initialise_migration_manager",
    "migrate_database",
    "rollback_database",
    "get_database_version",
    "create_migration",
]
