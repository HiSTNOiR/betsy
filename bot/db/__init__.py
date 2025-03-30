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

__all__ = [
    # Classes
    "Database",

    # Exceptions
    "DatabaseError",
    "ConnectionError",
    "TransactionError",
    "QueryError",

    # Functions
    "initialise_db_connection",
    "get_db",
    "close_db_connection",
    "db_transaction",
    "with_db",
]
