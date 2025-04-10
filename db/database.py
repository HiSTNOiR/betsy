import os
import sqlite3
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Union

from utils.platform_connections import SafeSingleton
from core.config import config
from core.logging import get_logger
from core.errors import DatabaseError, handle_error

logger = get_logger("database")


class Database(SafeSingleton):
    def _safe_init(self):
        self.db_path = config.get_path('DB_PATH', 'db/bot.db')
        self.schema_path = config.get_path(
            'SCHEMA_PATH', 'db/migrations/schema.sql')
        self.seed_path = config.get_path('SEED_PATH', 'db/migrations/seed.sql')
        self.enabled = config.get_boolean('DB_ENABLED', True)
        self.connection_pool = {}
        self.connection_pool_lock = threading.Lock()

        if self.enabled:
            try:
                self._ensure_db_directory()
                self._init_database()
            except Exception as e:
                handle_error(DatabaseError(
                    f"Failed to initialise database: {e}"))

    def _ensure_db_directory(self):
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def _init_database(self):
        if not os.path.exists(self.db_path):
            logger.info(f"Creating new database at {self.db_path}")
            self._create_database()
        else:
            logger.info(f"Database already exists at {self.db_path}")

    def _create_database(self):
        if not os.path.exists(self.schema_path):
            error_msg = f"Schema file not found: {self.schema_path}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)

        try:
            conn = self._get_connection()

            # Create schema
            with open(self.schema_path, 'r') as f:
                schema_sql = f.read()

            conn.executescript(schema_sql)
            logger.info("Database schema created successfully")

            # Apply seed data if available
            if os.path.exists(self.seed_path):
                with open(self.seed_path, 'r') as f:
                    seed_sql = f.read()

                try:
                    conn.executescript(seed_sql)
                    logger.info("Seed data applied successfully")
                except sqlite3.IntegrityError as e:
                    conn.rollback()
                    logger.warning(
                        f"Some seed data already exists, skipping: {e}")
                except Exception as e:
                    conn.rollback()
                    logger.error(f"Error applying seed data: {e}")
                    raise

        except sqlite3.Error as e:
            error_msg = f"Error creating database: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)

    def _get_connection(self) -> sqlite3.Connection:
        thread_id = threading.get_ident()

        with self.connection_pool_lock:
            if thread_id not in self.connection_pool:
                try:
                    conn = sqlite3.connect(
                        self.db_path,
                        check_same_thread=False,
                        isolation_level=None,
                        timeout=30.0
                    )
                    conn.row_factory = sqlite3.Row

                    # Enable foreign keys
                    conn.execute("PRAGMA foreign_keys = ON")

                    self.connection_pool[thread_id] = {
                        "connection": conn,
                        "lock": threading.Lock(),
                        "in_transaction": False
                    }
                    logger.debug(
                        f"Created new database connection for thread {thread_id}")
                except sqlite3.Error as e:
                    error_msg = f"Error connecting to database: {e}"
                    logger.error(error_msg)
                    raise DatabaseError(error_msg)

        return self.connection_pool[thread_id]["connection"]

    def safe_seed(self, table_name, unique_column, records):
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")

        for record in records:
            # Skip if record with this unique value already exists
            if unique_column in record:
                existing = self.fetchone(
                    f"SELECT 1 FROM {table_name} WHERE {unique_column} = ?",
                    (record[unique_column],)
                )
                if existing:
                    continue

            # Build dynamic INSERT statement based on record keys
            columns = ", ".join(record.keys())
            placeholders = ", ".join(["?" for _ in record])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            try:
                self.execute(query, list(record.values()))
            except Exception as e:
                # Log the error but continue with other records
                logger.warning(f"Failed to insert record in {table_name}: {e}")

    def execute(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None) -> sqlite3.Cursor:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")

        try:
            thread_id = threading.get_ident()
            conn_info = self.connection_pool.get(thread_id)

            if not conn_info:
                conn_info = self.connection_pool[thread_id] = {
                    "connection": self._get_connection(),
                    "lock": threading.Lock(),
                    "in_transaction": False
                }

            with conn_info["lock"]:
                if params is None:
                    return conn_info["connection"].execute(query)
                return conn_info["connection"].execute(query, params)
        except sqlite3.IntegrityError as e:
            # For integrity errors, log and reraise but with more context
            error_msg = f"Integrity constraint failed: {e}"
            logger.warning(error_msg)
            raise DatabaseError(error_msg, {"query": query})
        except sqlite3.Error as e:
            error_msg = f"Error executing query: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)

    def execute_many(self, query: str, params_list: List[Union[Dict[str, Any], List[Any], Tuple[Any, ...]]]) -> sqlite3.Cursor:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")

        try:
            thread_id = threading.get_ident()
            conn_info = self.connection_pool.get(thread_id)

            if not conn_info:
                conn_info = self.connection_pool[thread_id] = {
                    "connection": self._get_connection(),
                    "lock": threading.Lock(),
                    "in_transaction": False
                }

            with conn_info["lock"]:
                return conn_info["connection"].executemany(query, params_list)
        except sqlite3.Error as e:
            error_msg = f"Error executing batch query: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)

    def fetchone(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def fetchall(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def begin_transaction(self) -> None:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")

        thread_id = threading.get_ident()
        conn_info = self.connection_pool.get(thread_id)

        if not conn_info:
            conn_info = self.connection_pool[thread_id] = {
                "connection": self._get_connection(),
                "lock": threading.Lock(),
                "in_transaction": False
            }

        with conn_info["lock"]:
            if not conn_info["in_transaction"]:
                self.execute("BEGIN TRANSACTION")
                conn_info["in_transaction"] = True

    def commit(self) -> None:
        if not self.enabled:
            return

        thread_id = threading.get_ident()
        conn_info = self.connection_pool.get(thread_id)

        if conn_info and conn_info["in_transaction"]:
            with conn_info["lock"]:
                try:
                    conn_info["connection"].execute("COMMIT")
                    conn_info["in_transaction"] = False
                except sqlite3.Error as e:
                    error_msg = f"Error committing transaction: {e}"
                    logger.error(error_msg)
                    raise DatabaseError(error_msg)

    def rollback(self) -> None:
        if not self.enabled:
            return

        thread_id = threading.get_ident()
        conn_info = self.connection_pool.get(thread_id)

        if conn_info and conn_info["in_transaction"]:
            with conn_info["lock"]:
                try:
                    conn_info["connection"].execute("ROLLBACK")
                    conn_info["in_transaction"] = False
                except sqlite3.Error as e:
                    error_msg = f"Error rolling back transaction: {e}"
                    logger.error(error_msg)

    def close(self) -> None:
        if not self.enabled:
            return

        thread_id = threading.get_ident()
        with self.connection_pool_lock:
            if thread_id in self.connection_pool:
                try:
                    conn_info = self.connection_pool[thread_id]
                    if conn_info["in_transaction"]:
                        conn_info["connection"].execute("ROLLBACK")
                    conn_info["connection"].close()
                    del self.connection_pool[thread_id]
                    logger.debug(
                        f"Closed database connection for thread {thread_id}")
                except sqlite3.Error as e:
                    logger.error(f"Error closing database connection: {e}")

    def close_all(self) -> None:
        if not self.enabled:
            return

        with self.connection_pool_lock:
            for thread_id, conn_info in list(self.connection_pool.items()):
                try:
                    if conn_info["in_transaction"]:
                        conn_info["connection"].execute("ROLLBACK")
                    conn_info["connection"].close()
                    logger.debug(
                        f"Closed database connection for thread {thread_id}")
                except sqlite3.Error as e:
                    logger.error(
                        f"Error closing database connection for thread {thread_id}: {e}")
            self.connection_pool.clear()

    def get_last_inserted_id(self) -> int:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")

        return self.fetchone("SELECT last_insert_rowid() as id")["id"]

    def table_exists(self, table_name: str) -> bool:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")

        result = self.fetchone(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,)
        )
        return bool(result)

    def backup_database(self, backup_path: Optional[str] = None) -> str:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")

        import shutil
        from datetime import datetime

        if not backup_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = config.get_path('DB_BACKUP_DIR', 'db/backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, f"db_backup_{timestamp}.db")

        try:
            # Close all connections first to ensure a clean backup
            self.close_all()

            # Copy the database file
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")

            return backup_path
        except Exception as e:
            error_msg = f"Error backing up database: {e}"
            logger.error(error_msg)
            raise DatabaseError(error_msg)


# Singleton instance
db = Database()


def get_db() -> Database:
    return db
