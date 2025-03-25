"""
Test foreign key enforcement in the transaction safety module.
"""

import sys
import os
import sqlite3
import tempfile
from pathlib import Path

# Add the module directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Import the module
from src.mcp_server_sqlite.transaction_safety import safe_execute_query

# Create a temporary test database file
temp_db = tempfile.NamedTemporaryFile(delete=False)
TEST_DB = temp_db.name
temp_db.close()

def setup_test_db():
    """Set up test database with tables and foreign keys"""
    # Use direct connection to setup the database
    conn = sqlite3.connect(TEST_DB)
    
    # Create parent table
    conn.execute("""
    CREATE TABLE parent (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)
    
    # Create child table with foreign key
    conn.execute("""
    CREATE TABLE child (
        id INTEGER PRIMARY KEY,
        parent_id INTEGER NOT NULL,
        description TEXT,
        FOREIGN KEY (parent_id) REFERENCES parent(id)
    )
    """)
    
    # Insert test data
    conn.execute("INSERT INTO parent (id, name) VALUES (1, 'Test Parent')")
    conn.commit()
    conn.close()
    
    print(f"Test database setup completed at {TEST_DB}")

def test_foreign_key_enforcement():
    """Test that foreign keys are enforced in the safe_execute_query function"""
    # Try to check if foreign keys are enabled
    try:
        result = safe_execute_query(TEST_DB, "PRAGMA foreign_keys")
        print(f"Foreign keys setting: {result}")
    except Exception as e:
        print(f"Error checking foreign keys setting: {e}")
        
    # Insert valid record (should succeed)
    try:
        result = safe_execute_query(
            TEST_DB,
            "INSERT INTO child (parent_id, description) VALUES (?, ?)",
            [1, "Valid child record"]
        )
        print(f"Valid insert succeeded: {result}")
    except Exception as e:
        print(f"ERROR: Valid insert failed: {e}")
    
    # Insert invalid record (should fail with foreign key constraint)
    try:
        result = safe_execute_query(
            TEST_DB,
            "INSERT INTO child (parent_id, description) VALUES (?, ?)",
            [999, "Invalid child record - should fail"]
        )
        print(f"ERROR: Invalid insert succeeded when it should have failed: {result}")
    except Exception as e:
        print(f"Foreign key constraint properly enforced: {e}")
        
    # Verify that the valid record was inserted
    try:
        result = safe_execute_query(
            TEST_DB,
            "SELECT * FROM child WHERE parent_id = 1"
        )
        print(f"Valid records found: {result}")
    except Exception as e:
        print(f"Error retrieving valid records: {e}")

def cleanup():
    """Clean up test database file"""
    if os.path.exists(TEST_DB):
        os.unlink(TEST_DB)
        print(f"Test database removed: {TEST_DB}")

if __name__ == "__main__":
    try:
        setup_test_db()
        test_foreign_key_enforcement()
    finally:
        cleanup()
