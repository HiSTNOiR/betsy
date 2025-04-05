import os
import unittest
import tempfile
import sqlite3

class TestSimpleDb(unittest.TestCase):
    def setUp(self):
        # Create a temp file for the database
        self.db_fd, self.db_path = tempfile.mkstemp()
        # Create a connection
        self.conn = sqlite3.connect(self.db_path)
        # Create test table
        self.conn.execute('''
            CREATE TABLE test_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                points INTEGER NOT NULL DEFAULT 0
            )
        ''')
        self.conn.commit()
    
    def tearDown(self):
        self.conn.close()
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_basic_operations(self):
        # Insert
        self.conn.execute("INSERT INTO test_users (username, points) VALUES (?, ?)", 
                        ("test_user", 100))
        self.conn.commit()
        
        # Query
        cursor = self.conn.execute("SELECT * FROM test_users WHERE username = ?", 
                                ("test_user",))
        user = cursor.fetchone()
        self.assertIsNotNone(user)
        self.assertEqual(user[1], "test_user")
        self.assertEqual(user[2], 100)
        
        # Update
        self.conn.execute("UPDATE test_users SET points = ? WHERE username = ?", 
                        (200, "test_user"))
        self.conn.commit()
        
        # Verify update
        cursor = self.conn.execute("SELECT points FROM test_users WHERE username = ?", 
                                ("test_user",))
        points = cursor.fetchone()[0]
        self.assertEqual(points, 200)
        
        # Delete
        self.conn.execute("DELETE FROM test_users WHERE username = ?", 
                        ("test_user",))
        self.conn.commit()
        
        # Verify deletion
        cursor = self.conn.execute("SELECT * FROM test_users WHERE username = ?", 
                                ("test_user",))
        user = cursor.fetchone()
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()