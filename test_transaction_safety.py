"""
Simple script to test transaction safety integration

This script connects to the actual database and runs a test transaction
to verify proper functioning of the transaction safety mechanism.
"""

import os
import sqlite3
import tempfile
from src.mcp_server_sqlite.transaction_safety import safe_execute_query

def test_transaction_safety():
    """Run a simple transaction safety test"""
    print("Testing transaction safety...")
    
    # Create a test database
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    db_path = temp_db.name
    temp_db.close()
    
    # Set up test data
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE test_safety (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()
    conn.close()
    
    # Test 1: Successful transaction
    print("\nTest 1: Successful transaction")
    result = safe_execute_query(
        db_path,
        "INSERT INTO test_safety (name) VALUES ('Test 1')"
    )
    print(f"Result: {result}")
    
    # Verify
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_safety")
    rows = cursor.fetchall()
    print(f"Database has {len(rows)} rows after successful transaction")
    conn.close()
    
    # Test 2: Failed transaction
    print("\nTest 2: Failed transaction (should roll back)")
    try:
        result = safe_execute_query(
            db_path,
            "INSERT INTO test_safety (id, name) VALUES (1, 'Will fail due to duplicate ID')"
        )
        print("ERROR: Test failed - transaction should have thrown an exception")
    except Exception as e:
        print(f"Expected error occurred: {e}")
    
    # Verify
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM test_safety")
    rows = cursor.fetchall()
    print(f"Database still has {len(rows)} rows after failed transaction (should still be 1)")
    conn.close()
    
    # Clean up
    os.unlink(db_path)
    print("\nTransaction safety test completed")

if __name__ == "__main__":
    test_transaction_safety()
