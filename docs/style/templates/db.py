import sqlite3

from typing import List, Dict, Any, Optional

from core.logging import get_logger
from core.errors import DatabaseError, handle_error
from db.database import db

logger = get_logger("db_module")

class DatabaseModule:
    def __init__(self):
        self.db = db

    def create_record(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            
            self.db.execute(query, list(data.values()))
            return self.db.get_last_inserted_id()
        except (sqlite3.Error, DatabaseError) as e:
            handle_error(DatabaseError(f"Failed to create record in {table}: {e}", {"data": data}))
            return None

    # EXAMPLE IMPLEMENTATION
    def example_method(self, param1: str, param2: int) -> List[Dict[str, Any]]:
        try:
            query = "SELECT * FROM example_table WHERE column1 = ? AND column2 > ?"
            return self.db.fetchall(query, (param1, param2))
        except (sqlite3.Error, DatabaseError) as e:
            handle_error(DatabaseError(f"Failed to fetch records: {e}", {"param1": param1, "param2": param2}))
            return []