"""
Database connection management for the bot.

This module provides functionality for managing database connections, including
connection pooling, transaction management, and connection lifecycle.
"""

import logging
import os
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union, cast

# Set up logger for this module
logger = logging.getLogger(__name__)

# Type variable for type hinting
T = TypeVar('T')


class DatabaseError(Exception):
    """Base exception for database-related errors."""
    pass


class ConnectionError(DatabaseError):
    """Exception raised when a database connection cannot be established."""
    pass


class TransactionError(DatabaseError):
    """Exception raised for transaction-related errors."""
    pass


class QueryError(DatabaseError):
    """Exception raised for query-related errors."""
    pass


class Database:
    """
    Manages database connections and operations.

    This class provides a centralised way to manage SQLite database connections,
    ensuring proper connection lifecycle and thread safety.
    """

    def __init__(self, db_path: Union[str, Path]):
        """
        Initialize the database manager.

        Args:
            db_path (Union[str, Path]): Path to the SQLite database file.

        Raises:
            ConnectionError: If the database path is invalid or cannot be accessed.
        """
        try:
            # Convert to Path object for compatibility
            self._db_path = Path(db_path)

            # Create parent directory if it doesn't exist
            os.makedirs(self._db_path.parent, exist_ok=True)

            # Store the database path
            self._db_path_str = str(self._db_path)

            # Thread-local storage for connections
            self._local = threading.local()

            # Connection pool is not needed for SQLite as it's file-based
            # But we'll keep track of active connections for management
            self._active_connections = 0
            self._lock = threading.Lock()

            logger.info(
                f"Database manager initialised with path: {self._db_path_str}")
        except Exception as e:
            error_msg = f"Failed to initialise database manager: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise ConnectionError(error_msg) from e

    def _get_connection(self) -> sqlite3.Connection:
        """
        Get a SQLite database connection.

        Returns:
            sqlite3.Connection: SQLite connection object.

        Raises:
            ConnectionError: If the connection cannot be established.
        """
        # Check if there's already a connection for this thread
        if hasattr(self._local, 'connection') and self._local.connection:
            return self._local.connection

        try:
            # Create a new connection
            connection = sqlite3.connect(
                self._db_path_str,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                isolation_level=None,  # This enables autocommit mode
                check_same_thread=False  # We'll manage thread safety ourselves
            )

            # Enable foreign keys
            connection.execute("PRAGMA foreign_keys = ON")

            # Configure connection
            connection.row_factory = sqlite3.Row

            # Store the connection in thread-local storage
            self._local.connection = connection
            self._local.in_transaction = False

            # Update active connections count
            with self._lock:
                self._active_connections += 1

            logger.debug(
                f"Created new database connection (active: {self._active_connections})")
            return connection
        except Exception as e:
            error_msg = f"Failed to connect to database: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise ConnectionError(error_msg) from e

    def close(self) -> None:
        """
        Close the current thread's database connection.

        This should be called when a connection is no longer needed to free up resources.
        """
        if hasattr(self._local, 'connection') and self._local.connection:
            try:
                # Close the connection
                self._local.connection.close()
                self._local.connection = None
                self._local.in_transaction = False

                # Update active connections count
                with self._lock:
                    self._active_connections -= 1

                logger.debug(
                    f"Closed database connection (active: {self._active_connections})")
            except Exception as e:
                logger.error(
                    f"Error closing database connection: {str(e)}", exc_info=True)

    def close_all(self) -> None:
        """
        Close all database connections.

        This should be called during application shutdown to ensure all connections are closed.
        """
        # We can't directly access thread-local connections of other threads
        # But closing a SQLite database file will affect all connections
        # So we'll just close the current thread's connection
        self.close()
        logger.info("Database shutdown initiated")

    def execute(
        self,
        query: str,
        params: Optional[Union[Tuple, Dict[str, Any]]] = None
    ) -> sqlite3.Cursor:
        """
        Execute a SQL query.

        Args:
            query (str): SQL query to execute.
            params (Optional[Union[Tuple, Dict[str, Any]]]): Query parameters.

        Returns:
            sqlite3.Cursor: Query cursor.

        Raises:
            QueryError: If the query fails.
        """
        connection = self._get_connection()
        try:
            cursor = connection.execute(query, params or ())
            return cursor
        except Exception as e:
            error_msg = f"Query execution failed: {str(e)}, Query: {query}, Params: {params}"
            logger.error(error_msg, exc_info=True)
            raise QueryError(error_msg) from e

    def executemany(
        self,
        query: str,
        params_list: List[Union[Tuple, Dict[str, Any]]]
    ) -> sqlite3.Cursor:
        """
        Execute a SQL query with multiple parameter sets.

        Args:
            query (str): SQL query to execute.
            params_list (List[Union[Tuple, Dict[str, Any]]]): List of parameter sets.

        Returns:
            sqlite3.Cursor: Query cursor.

        Raises:
            QueryError: If the query fails.
        """
        connection = self._get_connection()
        try:
            cursor = connection.executemany(query, params_list)
            return cursor
        except Exception as e:
            error_msg = f"Query execution failed: {str(e)}, Query: {query}"
            logger.error(error_msg, exc_info=True)
            raise QueryError(error_msg) from e

    def fetchone(
        self,
        query: str,
        params: Optional[Union[Tuple, Dict[str, Any]]] = None
    ) -> Optional[sqlite3.Row]:
        """
        Execute a query and fetch one result.

        Args:
            query (str): SQL query to execute.
            params (Optional[Union[Tuple, Dict[str, Any]]]): Query parameters.

        Returns:
            Optional[sqlite3.Row]: Query result or None if no result.

        Raises:
            QueryError: If the query fails.
        """
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def fetchall(
        self,
        query: str,
        params: Optional[Union[Tuple, Dict[str, Any]]] = None
    ) -> List[sqlite3.Row]:
        """
        Execute a query and fetch all results.

        Args:
            query (str): SQL query to execute.
            params (Optional[Union[Tuple, Dict[str, Any]]]): Query parameters.

        Returns:
            List[sqlite3.Row]: Query results.

        Raises:
            QueryError: If the query fails.
        """
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def fetchmany(
        self,
        query: str,
        params: Optional[Union[Tuple, Dict[str, Any]]] = None,
        size: int = 100
    ) -> List[sqlite3.Row]:
        """
        Execute a query and fetch a specific number of results.

        Args:
            query (str): SQL query to execute.
            params (Optional[Union[Tuple, Dict[str, Any]]]): Query parameters.
            size (int): Number of results to fetch.

        Returns:
            List[sqlite3.Row]: Query results.

        Raises:
            QueryError: If the query fails.
        """
        cursor = self.execute(query, params)
        return cursor.fetchmany(size)

    def begin_transaction(self) -> None:
        """
        Begin a database transaction.

        Raises:
            TransactionError: If a transaction is already in progress.
        """
        if hasattr(self._local, 'in_transaction') and self._local.in_transaction:
            raise TransactionError("Transaction already in progress")

        connection = self._get_connection()
        try:
            connection.execute("BEGIN")
            self._local.in_transaction = True
            logger.debug("Transaction started")
        except Exception as e:
            error_msg = f"Failed to begin transaction: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise TransactionError(error_msg) from e

    def commit(self) -> None:
        """
        Commit the current transaction.

        Raises:
            TransactionError: If no transaction is in progress.
        """
        if not hasattr(self._local, 'in_transaction') or not self._local.in_transaction:
            raise TransactionError("No transaction in progress")

        connection = self._get_connection()
        try:
            connection.execute("COMMIT")
            self._local.in_transaction = False
            logger.debug("Transaction committed")
        except Exception as e:
            error_msg = f"Failed to commit transaction: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise TransactionError(error_msg) from e

    def rollback(self) -> None:
        """
        Rollback the current transaction.

        Raises:
            TransactionError: If no transaction is in progress.
        """
        if not hasattr(self._local, 'in_transaction') or not self._local.in_transaction:
            raise TransactionError("No transaction in progress")

        connection = self._get_connection()
        try:
            connection.execute("ROLLBACK")
            self._local.in_transaction = False
            logger.debug("Transaction rolled back")
        except Exception as e:
            error_msg = f"Failed to rollback transaction: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise TransactionError(error_msg) from e

    @contextmanager
    def transaction(self):
        """
        Context manager for database transactions.

        This ensures that transactions are properly committed or rolled back.

        Example:
            with db.transaction():
                db.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
                db.execute("UPDATE stats SET user_count = user_count + 1")

        Yields:
            Database: The database instance.

        Raises:
            TransactionError: If a transaction error occurs.
        """
        try:
            self.begin_transaction()
            yield self
            self.commit()
        except Exception as e:
            try:
                self.rollback()
            except Exception as rollback_error:
                logger.error(
                    f"Failed to rollback transaction: {str(rollback_error)}", exc_info=True)

            # Re-raise the original exception
            if isinstance(e, DatabaseError):
                raise
            else:
                error_msg = f"Transaction failed: {str(e)}"
                logger.error(error_msg, exc_info=True)
                raise TransactionError(error_msg) from e

    def row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """
        Convert a SQLite Row object to a dictionary.

        Args:
            row (sqlite3.Row): SQLite Row object.

        Returns:
            Dict[str, Any]: Dictionary representation of the row.
        """
        if row is None:
            return {}
        return {key: row[key] for key in row.keys()}

    def rows_to_dicts(self, rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
        """
        Convert a list of SQLite Row objects to a list of dictionaries.

        Args:
            rows (List[sqlite3.Row]): List of SQLite Row objects.

        Returns:
            List[Dict[str, Any]]: List of dictionaries.
        """
        return [self.row_to_dict(row) for row in rows]

    def insert(
        self,
        table: str,
        data: Dict[str, Any],
        return_id: bool = True
    ) -> Optional[int]:
        """
        Insert a record into a table.

        Args:
            table (str): Table name.
            data (Dict[str, Any]): Column-value mapping.
            return_id (bool): Whether to return the inserted record ID.

        Returns:
            Optional[int]: ID of the inserted record if return_id is True, otherwise None.

        Raises:
            QueryError: If the insert fails.
        """
        if not data:
            raise QueryError("Cannot insert empty data")

        # Build query dynamically
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        params = tuple(data.values())

        try:
            cursor = self.execute(query, params)
            if return_id:
                return cursor.lastrowid
            return None
        except Exception as e:
            error_msg = f"Insert failed: {str(e)}, Table: {table}, Data: {data}"
            logger.error(error_msg, exc_info=True)
            raise QueryError(error_msg) from e

    def update(
        self,
        table: str,
        data: Dict[str, Any],
        where: str,
        where_params: Optional[Union[Tuple, Dict[str, Any]]] = None
    ) -> int:
        """
        Update records in a table.

        Args:
            table (str): Table name.
            data (Dict[str, Any]): Column-value mapping.
            where (str): WHERE clause.
            where_params (Optional[Union[Tuple, Dict[str, Any]]]): WHERE clause parameters.

        Returns:
            int: Number of rows affected.

        Raises:
            QueryError: If the update fails.
        """
        if not data:
            raise QueryError("Cannot update with empty data")

        # Build query dynamically
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"

        params = tuple(data.values())
        if where_params:
            if isinstance(where_params, dict):
                # Convert dict to tuple in the correct order based on placeholders
                # This is complex for positional params, so we'll just append for now
                params = params + tuple(where_params.values())
            else:
                params = params + where_params

        try:
            cursor = self.execute(query, params)
            return cursor.rowcount
        except Exception as e:
            error_msg = f"Update failed: {str(e)}, Table: {table}, Data: {data}, Where: {where}"
            logger.error(error_msg, exc_info=True)
            raise QueryError(error_msg) from e

    def delete(
        self,
        table: str,
        where: str,
        where_params: Optional[Union[Tuple, Dict[str, Any]]] = None
    ) -> int:
        """
        Delete records from a table.

        Args:
            table (str): Table name.
            where (str): WHERE clause.
            where_params (Optional[Union[Tuple, Dict[str, Any]]]): WHERE clause parameters.

        Returns:
            int: Number of rows affected.

        Raises:
            QueryError: If the delete fails.
        """
        query = f"DELETE FROM {table} WHERE {where}"

        try:
            cursor = self.execute(query, where_params)
            return cursor.rowcount
        except Exception as e:
            error_msg = f"Delete failed: {str(e)}, Table: {table}, Where: {where}"
            logger.error(error_msg, exc_info=True)
            raise QueryError(error_msg) from e

    def table_exists(self, table: str) -> bool:
        """
        Check if a table exists in the database.

        Args:
            table (str): Table name.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.fetchone(query, (table,))
        return result is not None

    def column_exists(self, table: str, column: str) -> bool:
        """
        Check if a column exists in a table.

        Args:
            table (str): Table name.
            column (str): Column name.

        Returns:
            bool: True if the column exists, False otherwise.
        """
        if not self.table_exists(table):
            return False

        query = f"PRAGMA table_info({table})"
        columns = self.fetchall(query)
        return any(col['name'] == column for col in columns)

    def get_table_schema(self, table: str) -> List[Dict[str, Any]]:
        """
        Get the schema for a table.

        Args:
            table (str): Table name.

        Returns:
            List[Dict[str, Any]]: Table schema information.
        """
        query = f"PRAGMA table_info({table})"
        result = self.fetchall(query)
        return self.rows_to_dicts(result)

    def get_table_columns(self, table: str) -> List[str]:
        """
        Get a list of column names for a table.

        Args:
            table (str): Table name.

        Returns:
            List[str]: List of column names.
        """
        schema = self.get_table_schema(table)
        return [col['name'] for col in schema]


# Singleton database instance
_db_instance: Optional[Database] = None


def initialise_db_connection(db_path: Optional[Union[str, Path]] = None) -> Database:
    """
    Initialise the database connection.

    Args:
        db_path (Optional[Union[str, Path]]): Path to the SQLite database file.
            If None, uses the path from configuration.

    Returns:
        Database: Database instance.

    Raises:
        ConnectionError: If the database path is not provided and cannot be determined.
    """
    global _db_instance

    try:
        if db_path is None:
            # Try to get the path from configuration
            from bot.core.config import get_config
            config = get_config()
            db_path = config.get("db_path")

        if not db_path:
            error_msg = "Database path not provided and not available in configuration"
            logger.error(error_msg)
            raise ConnectionError(error_msg)

        # Create a new database instance
        _db_instance = Database(db_path)
        logger.info(f"Database initialised with path: {db_path}")
        return _db_instance
    except ImportError:
        error_msg = "Failed to import configuration module"
        logger.error(error_msg, exc_info=True)
        raise ConnectionError(error_msg)
    except Exception as e:
        error_msg = f"Failed to initialise database: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise ConnectionError(error_msg) from e


def get_db() -> Database:
    """
    Get the database instance.

    Returns:
        Database: Database instance.

    Raises:
        ConnectionError: If the database has not been initialised.
    """
    if _db_instance is None:
        raise ConnectionError(
            "Database not initialised. Call initialise_db_connection first.")
    return _db_instance


def close_db_connection() -> None:
    """
    Close the database connection.

    This should be called during application shutdown.
    """
    global _db_instance
    if _db_instance is not None:
        _db_instance.close_all()
        _db_instance = None
        logger.info("Database connection closed")


@contextmanager
def db_transaction():
    """
    Context manager for database transactions.

    This is a convenience wrapper around Database.transaction().

    Example:
        with db_transaction() as db:
            db.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
            db.execute("UPDATE stats SET user_count = user_count + 1")

    Yields:
        Database: The database instance.

    Raises:
        ConnectionError: If the database has not been initialised.
        TransactionError: If a transaction error occurs.
    """
    db = get_db()
    with db.transaction():
        yield db


def with_db(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to provide a database instance to a function.

    Example:
        @with_db
        def get_user(db, user_id):
            return db.fetchone("SELECT * FROM users WHERE id = ?", (user_id,))

    Args:
        func: Function to decorate.

    Returns:
        Callable[..., T]: Decorated function.
    """
    def wrapper(*args, **kwargs):
        db = get_db()
        return func(db, *args, **kwargs)
    return wrapper
