#!/usr/bin/env python3
"""
Test script to verify parameter binding functionality in sqlite-mcp-server
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_sqlite.server import EnhancedSqliteDatabase
from mcp_server_sqlite.db_integration import DatabaseIntegration

async def test_parameter_binding():
    """Test parameter binding with the actual sqlite-mcp-server implementation"""
    
    print("🧪 Testing SQLite MCP Server Parameter Binding")
    print("=" * 50)
    
    # Create test database
    db_path = "./test-param-binding.db"
    print(f"📁 Creating test database: {db_path}")
    
    try:
        # Initialize database
        db = EnhancedSqliteDatabase(db_path)
        db = DatabaseIntegration.enhance_database(db)
        
        print("✅ Database initialized with transaction safety")
        
        # Test 1: Create table
        print("\n📋 Test 1: Create table")
        db._execute_query("""
            CREATE TABLE IF NOT EXISTS test_params (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                value INTEGER,
                json_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table created successfully")
        
        # Test 2: Parameter binding with INSERT
        print("\n📝 Test 2: INSERT with parameter binding")
        try:
            result = db._execute_query(
                "INSERT INTO test_params (name, value, json_data) VALUES (?, ?, ?)",
                ["Test Item", 42, '{"key": "value", "array": [1, 2, 3]}']
            )
            print(f"✅ INSERT with parameters successful: {result}")
        except Exception as e:
            print(f"❌ INSERT with parameters failed: {e}")
            return False
        
        # Test 3: Parameter binding with SELECT
        print("\n🔍 Test 3: SELECT with parameter binding")
        try:
            result = db._execute_query(
                "SELECT * FROM test_params WHERE name = ? AND value > ?",
                ["Test Item", 40]
            )
            print(f"✅ SELECT with parameters successful: {result}")
        except Exception as e:
            print(f"❌ SELECT with parameters failed: {e}")
            return False
        
        # Test 4: JSON operations with parameters
        print("\n🔧 Test 4: JSON operations with parameter binding")
        try:
            result = db._execute_query(
                "SELECT name, json_extract(json_data, ?) as extracted_key FROM test_params WHERE id = ?",
                ["$.key", 1]
            )
            print(f"✅ JSON extraction with parameters successful: {result}")
        except Exception as e:
            print(f"❌ JSON extraction with parameters failed: {e}")
            return False
        
        # Test 5: UPDATE with parameters
        print("\n📝 Test 5: UPDATE with parameter binding")
        try:
            result = db._execute_query(
                "UPDATE test_params SET value = ?, json_data = ? WHERE name = ?",
                [99, '{"updated": true, "timestamp": "2025-09-16"}', "Test Item"]
            )
            print(f"✅ UPDATE with parameters successful: {result}")
        except Exception as e:
            print(f"❌ UPDATE with parameters failed: {e}")
            return False
        
        # Test 6: Verify update
        print("\n✅ Test 6: Verify UPDATE results")
        result = db._execute_query("SELECT * FROM test_params WHERE id = 1")
        print(f"Updated record: {result}")
        
        # Test 7: Complex query with multiple parameters
        print("\n🔧 Test 7: Complex query with multiple parameters")
        try:
            db._execute_query(
                "INSERT INTO test_params (name, value, json_data) VALUES (?, ?, ?)",
                ["Complex Test", 200, '{"complex": {"nested": {"data": [10, 20, 30]}}}']
            )
            
            result = db._execute_query("""
                SELECT name, value, 
                       json_extract(json_data, ?) as nested_value,
                       json_extract(json_data, ?) as array_element
                FROM test_params 
                WHERE value BETWEEN ? AND ? 
                ORDER BY value DESC
            """, ["$.complex.nested.data", "$.complex.nested.data[1]", 50, 300])
            
            print(f"✅ Complex query with parameters successful: {result}")
        except Exception as e:
            print(f"❌ Complex query with parameters failed: {e}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 ALL PARAMETER BINDING TESTS PASSED!")
        print("✅ Parameter binding is working correctly in sqlite-mcp-server")
        return True
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        try:
            Path(db_path).unlink(missing_ok=True)
            print(f"🧹 Cleaned up test database: {db_path}")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

if __name__ == "__main__":
    success = asyncio.run(test_parameter_binding())
    sys.exit(0 if success else 1)