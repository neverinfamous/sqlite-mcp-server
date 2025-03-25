"""
Tests for the transaction safety implementation
"""

import os
import sys
import sqlite3
import tempfile
import unittest
from pathlib import Path

# Add the parent directory to the path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.mcp_server_sqlite.transaction_safety import safe_execute_query

class TestTransactionSafety(unittest.TestCase):
    """Test the transaction safety mechanisms"""
    
    def setUp(self):
        """Set up a temporary database for testing"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        
        # Create a test table
        conn = sqlite3.connect(self.db_path)
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        conn.close()
    
    def tearDown(self):
        """Clean up the temporary database"""
        os.unlink(self.db_path)
    
    def test_successful_transaction(self):
        """Test that a successful transaction commits properly"""
        # Insert a row
        result = safe_execute_query(
            self.db_path, 
            "INSERT INTO test (name) VALUES (?)",
            ["Test Name"]
        )
        
        # Verify it was inserted
        self.assertEqual(result[0]["affected_rows"], 1)
        
        # Check that the row exists
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test")
        rows = cursor.fetchall()
        conn.close()
        
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Test Name")
    
    def test_failed_transaction(self):
        """Test that a failed transaction is rolled back"""
        # Initial state - insert a valid row
        safe_execute_query(
            self.db_path, 
            "INSERT INTO test (name) VALUES (?)",
            ["Valid Name"]
        )
        
        # Try to insert an invalid row that will cause a constraint violation
        try:
            safe_execute_query(
                self.db_path, 
                "INSERT INTO test (id, name) VALUES (?, ?), (?, ?)",
                [1, "Duplicate ID", 1, "This will fail"]
            )
            self.fail("Expected an exception")
        except:
            # Exception expected
            pass
        
        # Check that the database still only has one row
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test")
        rows = cursor.fetchall()
        conn.close()
        
        # There should only be one row - the valid one
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Valid Name")
    
    def test_read_query(self):
        """Test that read queries work as expected"""
        # Insert some test data
        safe_execute_query(
            self.db_path, 
            "INSERT INTO test (name) VALUES (?), (?)",
            ["Name 1", "Name 2"]
        )
        
        # Test the read query
        result = safe_execute_query(
            self.db_path, 
            "SELECT * FROM test"
        )
        
        # Verify the results
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Name 1")
        self.assertEqual(result[1]["name"], "Name 2")

if __name__ == "__main__":
    unittest.main()
