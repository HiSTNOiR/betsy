import threading
from typing import Any, Dict, List, Optional, Tuple, Union, Callable

from utils.platform_connections import SafeSingleton
from core.errors import DatabaseError, handle_error
from core.logging import get_logger
from core.config import config

logger = get_logger("db_manager")

class DatabaseEventManager(SafeSingleton):
    def _safe_init(self):
        self._subscribers = {}
        self._subscribers_lock = threading.Lock()
        self.enabled = config.get_boolean('DB_ENABLED', True)

        # Deferred import to avoid circular dependencies
        from data.database import get_db
        self.db = get_db()
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        with self._subscribers_lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            if callback not in self._subscribers[event_type]:
                self._subscribers[event_type].append(callback)
                logger.debug(f"Subscribed to database event: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        with self._subscribers_lock:
            if event_type in self._subscribers and callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
                logger.debug(f"Unsubscribed from database event: {event_type}")
    
    def publish(self, event_type: str, data: Dict[str, Any]) -> None:
        subscribers = []
        with self._subscribers_lock:
            if event_type in self._subscribers:
                subscribers = self._subscribers[event_type].copy()
        
        for callback in subscribers:
            try:
                callback(data)
            except Exception as e:
                handle_error(
                    DatabaseError(f"Error in database event callback: {e}"), 
                    {"event_type": event_type, "callback": str(callback)}
                )
    
    def execute(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None, 
                publish_event: bool = True, event_data: Optional[Dict[str, Any]] = None) -> Any:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
            
        try:
            cursor = self.db.execute(query, params)
            self.db.commit()
            
            if publish_event:
                event_type = self._get_event_type(query)
                event_info = event_data or {}
                event_info.update({
                    "query": query,
                    "params": params,
                    "affected_rows": cursor.rowcount
                })
                self.publish(event_type, event_info)
                
                # Also publish a generic event
                self.publish("database_changed", event_info)
            
            return cursor
        except Exception as e:
            logger.error(f"Database execution error: {e}")
            self.db.rollback()
            raise
    
    def execute_many(self, query: str, params_list: List[Union[Dict[str, Any], List[Any], Tuple[Any, ...]]],
                    publish_event: bool = True, event_data: Optional[Dict[str, Any]] = None) -> Any:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
            
        try:
            cursor = self.db.execute_many(query, params_list)
            self.db.commit()
            
            if publish_event:
                event_type = self._get_event_type(query)
                event_info = event_data or {}
                event_info.update({
                    "query": query,
                    "batch_size": len(params_list),
                    "affected_rows": cursor.rowcount
                })
                self.publish(event_type, event_info)
                
                # Also publish a generic event
                self.publish("database_changed", event_info)
            
            return cursor
        except Exception as e:
            logger.error(f"Database batch execution error: {e}")
            self.db.rollback()
            raise
    
    def fetchone(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
        return self.db.fetchone(query, params)
    
    def fetchall(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
        return self.db.fetchall(query, params)

    def begin_transaction(self) -> None:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
        self.db.begin_transaction()
        self.publish("transaction_started", {})

    def commit(self) -> None:
        if not self.enabled:
            return
        self.db.commit()
        self.publish("transaction_committed", {})

    def rollback(self) -> None:
        if not self.enabled:
            return
        self.db.rollback()
        self.publish("transaction_rolled_back", {})
    
    def table_exists(self, table_name: str) -> bool:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
        return self.db.table_exists(table_name)
    
    def get_last_inserted_id(self) -> int:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
        return self.db.get_last_inserted_id()
    
    def backup_database(self, backup_path: Optional[str] = None) -> str:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
        result = self.db.backup_database(backup_path)
        self.publish("database_backed_up", {"backup_path": result})
        return result
    
    def close(self) -> None:
        if not self.enabled:
            return
        self.db.close()
    
    def close_all(self) -> None:
        if not self.enabled:
            return
        self.db.close_all()
    
    def safe_seed(self, table_name, unique_column, records) -> None:
        if not self.enabled:
            raise DatabaseError("Database operations are disabled")
        self.db.safe_seed(table_name, unique_column, records)
        self.publish("database_seeded", {
            "table": table_name,
            "records_count": len(records)
        })

    def _get_event_type(self, query: str) -> str:
        query = query.strip().upper()
        
        if query.startswith("INSERT"):
            return "row_inserted"
        elif query.startswith("UPDATE"):
            return "row_updated"
        elif query.startswith("DELETE"):
            return "row_deleted"
        elif query.startswith("CREATE"):
            return "schema_changed"
        elif query.startswith("ALTER"):
            return "schema_changed"
        elif query.startswith("DROP"):
            return "schema_changed"
        else:
            return "query_executed"

# Create singleton instance
db_manager = DatabaseEventManager()

def get_db_manager() -> DatabaseEventManager:
    return db_manager