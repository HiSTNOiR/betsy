"""
Unit tests for database connection management.

This module tests the functionality of the database connection manager.
"""

import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from bot.db.connection import (
    Database,
    ConnectionError,
    QueryError,
    TransactionError,
    initialise_db_connection,
    get_db,
    close_db_connection,
    db_transaction,
    with_db,
)


class TestDatabase(unittest.TestCase):
    """Tests for the Database class."""

    def setUp(self):
        """Set up test database."""
        # Create a temporary database file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"
        self.db = Database(self.db_path)

        # Create a test table
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                value INTEGER
            )
        """)

    def tearDown(self):
        """Clean up after tests."""
        self.db.close_all()
        self.temp_dir.cleanup()

    def test_init(self):
        """Test database initialisation."""
        # Check that the database file was created
        self.assertTrue(self.db_path.exists())

        # Check that the connection is working
        result = self.db.fetchone("SELECT sqlite_version()")
        self.assertIsNotNone(result)

    def test_init_with_invalid_path(self):
        """Test initialisation with invalid path."""
        with self.assertRaises(ConnectionError):
            # Try to create a database in a non-existent directory with illegal characters
            Database("/not/a/valid/path/|*?<>:\\/test.db")

    def test_execute(self):
        """Test query execution."""
        # Insert a record
        self.db.execute(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            ("test", 42)
        )

        # Check that the record was inserted
        result = self.db.fetchone(
            "SELECT id, name, value FROM test_table WHERE name = ?",
            ("test",)
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "test")
        self.assertEqual(result["value"], 42)

    def test_execute_with_invalid_query(self):
        """Test execution with invalid query."""
        with self.assertRaises(QueryError):
            self.db.execute("SELECT * FROM non_existent_table")

    def test_executemany(self):
        """Test executing multiple queries."""
        # Insert multiple records
        data = [
            ("item1", 10),
            ("item2", 20),
            ("item3", 30)
        ]
        self.db.executemany(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            data
        )

        # Check that all records were inserted
        results = self.db.fetchall(
            "SELECT name, value FROM test_table ORDER BY id")
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["name"], "item1")
        self.assertEqual(results[1]["name"], "item2")
        self.assertEqual(results[2]["name"], "item3")

    def test_fetchone(self):
        """Test fetching a single result."""
        # Insert a record
        self.db.execute(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            ("single", 100)
        )

        # Fetch the record
        result = self.db.fetchone(
            "SELECT id, name, value FROM test_table WHERE name = ?",
            ("single",)
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "single")
        self.assertEqual(result["value"], 100)

        # Test fetching non-existent record
        result = self.db.fetchone(
            "SELECT id FROM test_table WHERE name = ?",
            ("non_existent",)
        )
        self.assertIsNone(result)

    def test_fetchall(self):
        """Test fetching all results."""
        # Insert multiple records
        data = [
            ("batch1", 1),
            ("batch1", 2),
            ("batch1", 3)
        ]
        self.db.executemany(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            data
        )

        # Fetch all matching records
        results = self.db.fetchall(
            "SELECT id, name, value FROM test_table WHERE name = ? ORDER BY value",
            ("batch1",)
        )
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["value"], 1)
        self.assertEqual(results[1]["value"], 2)
        self.assertEqual(results[2]["value"], 3)

        # Test fetching with no matching records
        results = self.db.fetchall(
            "SELECT id FROM test_table WHERE name = ?",
            ("non_existent",)
        )
        self.assertEqual(len(results), 0)

    def test_fetchmany(self):
        """Test fetching a limited number of results."""
        # Insert multiple records
        data = [
            ("batch2", 1),
            ("batch2", 2),
            ("batch2", 3),
            ("batch2", 4),
            ("batch2", 5)
        ]
        self.db.executemany(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            data
        )

        # Fetch a subset of matching records
        results = self.db.fetchmany(
            "SELECT id, name, value FROM test_table WHERE name = ? ORDER BY value",
            ("batch2",),
            size=3
        )
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["value"], 1)
        self.assertEqual(results[1]["value"], 2)
        self.assertEqual(results[2]["value"], 3)

    def test_transaction(self):
        """Test transaction context manager."""
        # Use transaction to insert records
        with self.db.transaction():
            self.db.execute(
                "INSERT INTO test_table (name, value) VALUES (?, ?)",
                ("tx1", 1)
            )
            self.db.execute(
                "INSERT INTO test_table (name, value) VALUES (?, ?)",
                ("tx1", 2)
            )

        # Check that records were committed
        results = self.db.fetchall(
            "SELECT name, value FROM test_table WHERE name = ? ORDER BY value",
            ("tx1",)
        )
        self.assertEqual(len(results), 2)

        # Test transaction rollback on exception
        try:
            with self.db.transaction():
                self.db.execute(
                    "INSERT INTO test_table (name, value) VALUES (?, ?)",
                    ("tx2", 1)
                )
                # This will cause an error
                self.db.execute(
                    "INSERT INTO non_existent_table (name) VALUES (?)",
                    ("error",)
                )
        except QueryError:
            pass

        # Check that no records were committed
        results = self.db.fetchall(
            "SELECT name, value FROM test_table WHERE name = ?",
            ("tx2",)
        )
        self.assertEqual(len(results), 0)

    def test_manual_transaction(self):
        """Test manual transaction management."""
        # Begin a transaction
        self.db.begin_transaction()

        # Execute some queries
        self.db.execute(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            ("manual_tx", 1)
        )
        self.db.execute(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            ("manual_tx", 2)
        )

        # Commit the transaction
        self.db.commit()

        # Check that records were committed
        results = self.db.fetchall(
            "SELECT name, value FROM test_table WHERE name = ? ORDER BY value",
            ("manual_tx",)
        )
        self.assertEqual(len(results), 2)

        # Test transaction rollback
        self.db.begin_transaction()
        self.db.execute(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            ("rollback", 1)
        )
        self.db.rollback()

        # Check that no records were committed
        results = self.db.fetchall(
            "SELECT name, value FROM test_table WHERE name = ?",
            ("rollback",)
        )
        self.assertEqual(len(results), 0)

    def test_transaction_errors(self):
        """Test transaction error handling."""
        # Begin a transaction
        self.db.begin_transaction()

        # Try to begin another transaction
        with self.assertRaises(TransactionError):
            self.db.begin_transaction()

        # Clean up
        self.db.rollback()

        # Try to commit without a transaction
        with self.assertRaises(TransactionError):
            self.db.commit()

        # Try to rollback without a transaction
        with self.assertRaises(TransactionError):
            self.db.rollback()

    def test_insert(self):
        """Test insert helper method."""
        # Insert a record
        record_id = self.db.insert(
            "test_table",
            {"name": "insert_test", "value": 42}
        )
        self.assertIsNotNone(record_id)

        # Check that the record was inserted
        result = self.db.fetchone(
            "SELECT id, name, value FROM test_table WHERE id = ?",
            (record_id,)
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "insert_test")
        self.assertEqual(result["value"], 42)

        # Test insert without returning ID
        self.db.insert(
            "test_table",
            {"name": "no_id", "value": 100},
            return_id=False
        )

        # Check that the record was inserted
        result = self.db.fetchone(
            "SELECT name, value FROM test_table WHERE name = ?",
            ("no_id",)
        )
        self.assertIsNotNone(result)
        self.assertEqual(result["value"], 100)

    def test_insert_with_empty_data(self):
        """Test insert with empty data."""
        with self.assertRaises(QueryError):
            self.db.insert("test_table", {})

    def test_update(self):
        """Test update helper method."""
        # Insert a record
        self.db.execute(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            ("update_test", 10)
        )

        # Update the record
        rows_affected = self.db.update(
            "test_table",
            {"value": 20},
            "name = ?",
            ("update_test",)
        )
        self.assertEqual(rows_affected, 1)

        # Check that the record was updated
        result = self.db.fetchone(
            "SELECT value FROM test_table WHERE name = ?",
            ("update_test",)
        )
        self.assertEqual(result["value"], 20)

        # Test update with no matching records
        rows_affected = self.db.update(
            "test_table",
            {"value": 30},
            "name = ?",
            ("non_existent",)
        )
        self.assertEqual(rows_affected, 0)

    def test_update_with_empty_data(self):
        """Test update with empty data."""
        with self.assertRaises(QueryError):
            self.db.update(
                "test_table",
                {},
                "name = ?",
                ("test",)
            )

    def test_delete(self):
        """Test delete helper method."""
        # Insert records
        self.db.executemany(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            [
                ("delete_test", 1),
                ("delete_test", 2),
                ("keep_test", 3)
            ]
        )

        # Delete specific records
        rows_affected = self.db.delete(
            "test_table",
            "name = ?",
            ("delete_test",)
        )
        self.assertEqual(rows_affected, 2)

        # Check that records were deleted
        results = self.db.fetchall(
            "SELECT name FROM test_table WHERE name = ?",
            ("delete_test",)
        )
        self.assertEqual(len(results), 0)

        # Check that other records were kept
        results = self.db.fetchall(
            "SELECT name FROM test_table WHERE name = ?",
            ("keep_test",)
        )
        self.assertEqual(len(results), 1)

        # Test delete with no matching records
        rows_affected = self.db.delete(
            "test_table",
            "name = ?",
            ("non_existent",)
        )
        self.assertEqual(rows_affected, 0)

    def test_table_exists(self):
        """Test table_exists method."""
        self.assertTrue(self.db.table_exists("test_table"))
        self.assertFalse(self.db.table_exists("non_existent_table"))

    def test_column_exists(self):
        """Test column_exists method."""
        self.assertTrue(self.db.column_exists("test_table", "name"))
        self.assertTrue(self.db.column_exists("test_table", "value"))
        self.assertFalse(self.db.column_exists(
            "test_table", "non_existent_column"))
        self.assertFalse(self.db.column_exists("non_existent_table", "column"))

    def test_get_table_schema(self):
        """Test get_table_schema method."""
        schema = self.db.get_table_schema("test_table")
        self.assertEqual(len(schema), 3)  # id, name, value

        # Check column definitions
        column_names = [col["name"] for col in schema]
        self.assertIn("id", column_names)
        self.assertIn("name", column_names)
        self.assertIn("value", column_names)

        # Check primary key
        pk_column = next(col for col in schema if col["pk"] == 1)
        self.assertEqual(pk_column["name"], "id")

    def test_get_table_columns(self):
        """Test get_table_columns method."""
        columns = self.db.get_table_columns("test_table")
        self.assertEqual(len(columns), 3)
        self.assertIn("id", columns)
        self.assertIn("name", columns)
        self.assertIn("value", columns)

    def test_row_to_dict(self):
        """Test row_to_dict method."""
        # Insert a record
        self.db.execute(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            ("dict_test", 42)
        )

        # Get the record as a Row object
        row = self.db.fetchone(
            "SELECT id, name, value FROM test_table WHERE name = ?",
            ("dict_test",)
        )

        # Convert to dict
        row_dict = self.db.row_to_dict(row)
        self.assertIsInstance(row_dict, dict)
        self.assertEqual(row_dict["name"], "dict_test")
        self.assertEqual(row_dict["value"], 42)

        # Test with None
        self.assertEqual(self.db.row_to_dict(None), {})

    def test_rows_to_dicts(self):
        """Test rows_to_dicts method."""
        # Insert records
        self.db.executemany(
            "INSERT INTO test_table (name, value) VALUES (?, ?)",
            [
                ("dicts_test1", 10),
                ("dicts_test2", 20)
            ]
        )

        # Get the records as Row objects
        rows = self.db.fetchall(
            "SELECT id, name, value FROM test_table WHERE name LIKE 'dicts_test%' ORDER BY value"
        )

        # Convert to list of dicts
        row_dicts = self.db.rows_to_dicts(rows)
        self.assertIsInstance(row_dicts, list)
        self.assertEqual(len(row_dicts), 2)
        self.assertEqual(row_dicts[0]["name"], "dicts_test1")
        self.assertEqual(row_dicts[1]["name"], "dicts_test2")
        self.assertEqual(row_dicts[0]["value"], 10)
        self.assertEqual(row_dicts[1]["value"], 20)


class TestDatabaseSingleton(unittest.TestCase):
    """Tests for database singleton functions."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary database file
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_singleton.db"

        # Mock the config module
        self.config_patcher = patch("bot.core.config.get_config")
        self.mock_config = self.config_patcher.start()

        # Configure the mock to return our test path
        mock_config_instance = MagicMock()
        mock_config_instance.get.return_value = str(self.db_path)
        self.mock_config.return_value = mock_config_instance

    def tearDown(self):
        """Clean up after tests."""
        # Stop the patchers
        self.config_patcher.stop()

        # Clean up the database
        close_db_connection()
        self.temp_dir.cleanup()

    def test_initialise_db_connection(self):
        """Test initialisation of database connection."""
        # Test with explicit path
        db = initialise_db_connection(self.db_path)
        self.assertIsInstance(db, Database)
        # Execute a query to ensure the file is created
        db.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY)")
        self.assertTrue(self.db_path.exists())
        close_db_connection()

        # Test with path from config
        db = initialise_db_connection()
        self.assertIsInstance(db, Database)
        # Execute a query to ensure the file is created
        db.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY)")
        self.assertTrue(self.db_path.exists())

    def test_get_db(self):
        """Test getting the database instance."""
        # First, try without initialising
        with self.assertRaises(ConnectionError):
            get_db()

        # Initialise the database
        initialise_db_connection(self.db_path)

        # Now get_db should work
        db = get_db()
        self.assertIsInstance(db, Database)

        # Getting it again should return the same instance
        db2 = get_db()
        self.assertIs(db, db2)

    def test_close_db_connection(self):
        """Test closing the database connection."""
        # Initialise the database
        initialise_db_connection(self.db_path)

        # Close the connection
        close_db_connection()

        # Trying to get the database should now fail
        with self.assertRaises(ConnectionError):
            get_db()

    def test_db_transaction_context_manager(self):
        """Test db_transaction context manager."""
        # Initialise the database
        db = initialise_db_connection(self.db_path)

        # Create a test table
        db.execute("""
            CREATE TABLE IF NOT EXISTS singleton_test (
                id INTEGER PRIMARY KEY,
                value TEXT
            )
        """)

        # Use db_transaction
        with db_transaction() as tx_db:
            tx_db.execute(
                "INSERT INTO singleton_test (value) VALUES (?)",
                ("transaction_test",)
            )

        # Check that the record was committed
        result = db.fetchone(
            "SELECT value FROM singleton_test WHERE value = ?",
            ("transaction_test",)
        )
        self.assertIsNotNone(result)

        # Test transaction rollback
        try:
            with db_transaction() as tx_db:
                tx_db.execute(
                    "INSERT INTO singleton_test (value) VALUES (?)",
                    ("rollback_test",)
                )
                # This will cause an error
                tx_db.execute(
                    "INSERT INTO non_existent_table (value) VALUES (?)",
                    ("error",)
                )
        except QueryError:
            pass

        # Check that the transaction was rolled back
        result = db.fetchone(
            "SELECT value FROM singleton_test WHERE value = ?",
            ("rollback_test",)
        )
        self.assertIsNone(result)

    def test_with_db_decorator(self):
        """Test with_db decorator."""
        # Initialise the database
        db = initialise_db_connection(self.db_path)

        # Create a test table
        db.execute("""
            CREATE TABLE IF NOT EXISTS decorator_test (
                id INTEGER PRIMARY KEY,
                value TEXT
            )
        """)

        # Define a function using the decorator
        @with_db
        def insert_value(db, value):
            db.execute(
                "INSERT INTO decorator_test (value) VALUES (?)",
                (value,)
            )
            return value

        # Define a function to retrieve the value
        @with_db
        def get_value(db, value):
            result = db.fetchone(
                "SELECT value FROM decorator_test WHERE value = ?",
                (value,)
            )
            return result["value"] if result else None

        # Test the decorated functions
        insert_value("decorator_test")
        self.assertEqual(get_value("decorator_test"), "decorator_test")
        self.assertIsNone(get_value("non_existent"))


if __name__ == "__main__":
    unittest.main()
