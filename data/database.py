import os
import sqlite3
import threading

from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Union

from core.config import config
from core.errors import DatabaseError, handle_error
from core.logging import get_logger

logger = get_logger("database")

class Database:
    _instance = None
    _lock = threading.Lock()
    _connections = {}
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._initialised = False
            return cls._instance
    
    def __init__(self):
        if not getattr(self, '_initialised', False):
            self.db_path = config.get_path('DB_PATH', 'data/db.db')
            self.schema_path = config.get_path('SCHEMA_PATH', 'migrations/schema.sql')
            self.seed_path = config.get_path('SEED_PATH', 'migrations/seed.sql')
            self.enabled = config.get_boolean('DB_ENABLED', True)
            self._initialised = True
            
            if self.enabled:
                try:
                    self._ensure_db_directory()
                    self._init_database()
                except Exception as e:
                    handle_error(DatabaseError(f"Failed to initialise database: {e}"))
    
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
        try:
            conn = self._get_connection()
            
            if os.path.exists(self.schema_path):
                with open(self.schema_path, 'r') as f:
                    schema_sql = f.read()
                    
                conn.executescript(schema_sql)
                logger.info("Database schema created successfully")
                
                # Apply seed data if available
                if os.path.exists(self.seed_path):
                    with open(self.seed_path, 'r') as f:
                        seed_sql = f.read()
                    
                    conn.executescript(seed_sql)
                    logger.info("Seed data applied successfully")
            else:
                raise DatabaseError(f"Schema file not found: {self.schema_path}")
                
        except sqlite3.Error as e:
            raise DatabaseError(f"Error creating database: {e}")
    
    def _get_connection(self) -> sqlite3.Connection:
        thread_id = threading.get_ident()
        
        if thread_id not in self._connections:
            try:
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.row_factory = sqlite3.Row
                self._connections[thread_id] = conn
                logger.debug(f"Created new database connection for thread {thread_id}")
            except sqlite3.Error as e:
                raise DatabaseError(f"Error connecting to database: {e}")
        
        return self._connections[thread_id]
    
    def execute(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None) -> sqlite3.Cursor:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
            
        try:
            conn = self._get_connection()
            if params is None:
                return conn.execute(query)
            return conn.execute(query, params)
        except sqlite3.Error as e:
            raise DatabaseError(f"Error executing query: {e}")
    
    def execute_many(self, query: str, params_list: List[Union[Dict[str, Any], List[Any], Tuple[Any, ...]]]) -> sqlite3.Cursor:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
            
        try:
            conn = self._get_connection()
            return conn.executemany(query, params_list)
        except sqlite3.Error as e:
            raise DatabaseError(f"Error executing batch query: {e}")
    
    def fetchone(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def fetchall(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def commit(self) -> None:
        if not self.enabled:
            return
            
        try:
            thread_id = threading.get_ident()
            if thread_id in self._connections:
                self._connections[thread_id].commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Error committing transaction: {e}")
    
    def rollback(self) -> None:
        if not self.enabled:
            return
            
        try:
            thread_id = threading.get_ident()
            if thread_id in self._connections:
                self._connections[thread_id].rollback()
        except sqlite3.Error as e:
            raise DatabaseError(f"Error rolling back transaction: {e}")
    
    def begin_transaction(self) -> None:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
            
        try:
            self.execute("BEGIN TRANSACTION")
        except sqlite3.Error as e:
            raise DatabaseError(f"Error beginning transaction: {e}")
    
    def close(self) -> None:
        if not self.enabled:
            return
            
        thread_id = threading.get_ident()
        if thread_id in self._connections:
            try:
                self._connections[thread_id].close()
                del self._connections[thread_id]
                logger.debug(f"Closed database connection for thread {thread_id}")
            except sqlite3.Error as e:
                logger.error(f"Error closing database connection: {e}")
    
    def close_all(self) -> None:
        if not self.enabled:
            return
            
        for thread_id, conn in list(self._connections.items()):
            try:
                conn.close()
                del self._connections[thread_id]
                logger.debug(f"Closed database connection for thread {thread_id}")
            except sqlite3.Error as e:
                logger.error(f"Error closing database connection for thread {thread_id}: {e}")
    
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
            backup_dir = config.get_path('DB_BACKUP_DIR', 'data/backups')
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, f"db_backup_{timestamp}.db")
        
        try:
            # Close all connections first
            self.close_all()
            
            # Copy the database file
            shutil.copy2(self.db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            
            return backup_path
        except Exception as e:
            raise DatabaseError(f"Error backing up database: {e}")

# Singleton instance
db = Database()

def get_db() -> Database:
    return db