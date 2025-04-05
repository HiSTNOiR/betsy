import os
import unittest
import tempfile

from pathlib import Path

from core.config import config
from data.database import Database
from data.db_manager import DatabaseEventManager

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test.db")
        self.schema_path = os.path.join(os.path.dirname(__file__), "../migrations/schema.sql")
        
        # Override configuration for testing
        config._config["DB_PATH"] = self.db_path
        config._config["SCHEMA_PATH"] = self.schema_path
        config._config["DB_ENABLED"] = True
        
        # Create a fresh instance for testing
        Database._instance = None
        self.db = Database()
    
    def tearDown(self):
        self.db.close_all()
        self.temp_dir.cleanup()
    
    def test_database_initialization(self):
        self.assertTrue(os.path.exists(self.db_path))
        
        # Check if tables were created
        tables = self.db.fetchall("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [table["name"] for table in tables]
        
        self.assertIn("users", table_names)
        self.assertIn("commands", table_names)
        self.assertIn("duels", table_names)
    
    def test_basic_crud_operations(self):
        # Test INSERT
        self.db.execute(
            "INSERT INTO users (twitch_user_id, twitch_username, date_added) VALUES (?, ?, datetime('now'))",
            ("123456", "test_user")
        )
        self.db.commit()
        
        # Test SELECT
        user = self.db.fetchone("SELECT * FROM users WHERE twitch_user_id = ?", ("123456",))
        self.assertIsNotNone(user)
        self.assertEqual(user["twitch_username"], "test_user")
        
        # Test UPDATE
        self.db.execute(
            "UPDATE users SET twitch_username = ? WHERE twitch_user_id = ?",
            ("updated_user", "123456")
        )
        self.db.commit()
        
        user = self.db.fetchone("SELECT * FROM users WHERE twitch_user_id = ?", ("123456",))
        self.assertEqual(user["twitch_username"], "updated_user")
        
        # Test DELETE
        self.db.execute("DELETE FROM users WHERE twitch_user_id = ?", ("123456",))
        self.db.commit()
        
        user = self.db.fetchone("SELECT * FROM users WHERE twitch_user_id = ?", ("123456",))
        self.assertIsNone(user)

class TestDatabaseEventManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test.db")
        self.schema_path = os.path.join(os.path.dirname(__file__), "../migrations/schema.sql")
        
        # Override configuration for testing
        config._config["DB_PATH"] = self.db_path
        config._config["SCHEMA_PATH"] = self.schema_path
        config._config["DB_ENABLED"] = True
        
        # Create fresh instances for testing
        Database._instance = None
        DatabaseEventManager._instance = None
        self.db_manager = DatabaseEventManager()
        
        self.events_received = []
    
    def tearDown(self):
        self.db_manager.db.close_all()
        self.temp_dir.cleanup()
    
    def event_callback(self, data):
        self.events_received.append(data)
    
    def test_event_subscription(self):
        self.db_manager.subscribe("row_inserted", self.event_callback)
        self.db_manager.subscribe("row_updated", self.event_callback)
        self.db_manager.subscribe("database_changed", self.event_callback)
        
        # Test INSERT event
        self.db_manager.execute(
            "INSERT INTO users (twitch_user_id, twitch_username, date_added) VALUES (?, ?, datetime('now'))",
            ("123456", "test_user")
        )
        
        self.assertEqual(len(self.events_received), 2)  # row_inserted and database_changed
        
        # Test UPDATE event
        self.events_received.clear()
        self.db_manager.execute(
            "UPDATE users SET twitch_username = ? WHERE twitch_user_id = ?",
            ("updated_user", "123456")
        )
        
        self.assertEqual(len(self.events_received), 2)  # row_updated and database_changed
        
        # Test unsubscribe
        self.events_received.clear()
        self.db_manager.unsubscribe("row_updated", self.event_callback)
        
        self.db_manager.execute(
            "UPDATE users SET twitch_username = ? WHERE twitch_user_id = ?",
            ("another_update", "123456")
        )
        
        self.assertEqual(len(self.events_received), 1)  # only database_changed

if __name__ == "__main__":
    unittest.main()