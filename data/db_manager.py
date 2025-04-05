from typing import Any, Dict, List, Optional, Tuple, Union, Callable

from core.errors import DatabaseError, handle_error
from core.logging import get_logger
from data.database import get_db

logger = get_logger("db_manager")

class DatabaseEventManager:
    _instance = None
    _subscribers = {}
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseEventManager, cls).__new__(cls)
            cls._instance._initialised = False
        return cls._instance
    
    def __init__(self):
        if not getattr(self, '_initialised', False):
            self.db = get_db()
            self._initialised = True
    
    def subscribe(self, event_type: str, callback: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        logger.debug(f"Subscribed to database event: {event_type}")
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        if event_type in self._subscribers and callback in self._subscribers[event_type]:
            self._subscribers[event_type].remove(callback)
            logger.debug(f"Unsubscribed from database event: {event_type}")
    
    def publish(self, event_type: str, data: Dict[str, Any]) -> None:
        if not self._subscribers.get(event_type):
            return
        
        for callback in self._subscribers[event_type]:
            try:
                callback(data)
            except Exception as e:
                handle_error(DatabaseError(f"Error in database event callback: {e}"), 
                            {"event_type": event_type, "callback": str(callback)})
    
    def execute(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None, 
                publish_event: bool = True, event_data: Optional[Dict[str, Any]] = None) -> Any:
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
            self.db.rollback()
            raise e
    
    def execute_many(self, query: str, params_list: List[Union[Dict[str, Any], List[Any], Tuple[Any, ...]]],
                    publish_event: bool = True, event_data: Optional[Dict[str, Any]] = None) -> Any:
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
            self.db.rollback()
            raise e
    
    def fetchone(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None) -> Optional[Dict[str, Any]]:
        return self.db.fetchone(query, params)
    
    def fetchall(self, query: str, params: Union[Dict[str, Any], List[Any], Tuple[Any, ...]] = None) -> List[Dict[str, Any]]:
        return self.db.fetchall(query, params)
    
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

db_manager = DatabaseEventManager()

def get_db_manager() -> DatabaseEventManager:
    return db_manager