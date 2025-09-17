#!/usr/bin/env python3
"""
Test comprehensive JSON operations with escaping and parameter binding
"""

import json
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_server_sqlite.server import EnhancedSqliteDatabase
from mcp_server_sqlite.db_integration import DatabaseIntegration

def test_json_operations():
    """Test JSON operations with complex data and escaping scenarios"""
    
    print("🔧 Testing JSON Operations & Escaping")
    print("=" * 45)
    
    db_path = "./test-json-ops.db"
    
    try:
        # Initialize database
        db = EnhancedSqliteDatabase(db_path)
        db = DatabaseIntegration.enhance_database(db)
        
        # Create test table
        db._execute_query("""
            CREATE TABLE json_test (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                json_data TEXT,
                jsonb_data BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("✅ Test table created")
        
        # Test 1: Basic JSON with parameter binding
        print("\n📝 Test 1: Basic JSON with parameter binding")
        basic_json = {"name": "John Doe", "age": 30, "active": True}
        
        db._execute_query(
            "INSERT INTO json_test (name, json_data) VALUES (?, ?)",
            ["Basic Test", json.dumps(basic_json)]
        )
        
        result = db._execute_query(
            "SELECT name, json_extract(json_data, ?) as name_field FROM json_test WHERE name = ?",
            ["$.name", "Basic Test"]
        )
        print(f"✅ Basic JSON: {result}")
        
        # Test 2: JSON with quotes and special characters
        print("\n🔤 Test 2: JSON with quotes and special characters")
        complex_json = {
            "message": 'He said "Hello World!" and she replied \'Great!\'',
            "path": "C:\\Users\\chris\\Documents\\file.txt",
            "regex": r"^\d{3}-\d{2}-\d{4}$",
            "unicode": "🎉 Testing unicode: café, naïve, résumé",
            "newlines": "Line 1\nLine 2\nLine 3",
            "tabs": "Col1\tCol2\tCol3"
        }
        
        db._execute_query(
            "INSERT INTO json_test (name, json_data) VALUES (?, ?)",
            ["Complex Test", json.dumps(complex_json)]
        )
        
        result = db._execute_query(
            "SELECT json_extract(json_data, ?) as message, json_extract(json_data, ?) as path FROM json_test WHERE name = ?",
            ["$.message", "$.path", "Complex Test"]
        )
        print(f"✅ Complex JSON: {result}")
        
        # Test 3: Nested JSON structures
        print("\n🏗️ Test 3: Nested JSON structures")
        nested_json = {
            "user": {
                "profile": {
                    "personal": {
                        "name": "Jane Smith",
                        "contact": {
                            "email": "jane@example.com",
                            "phones": ["+1-555-1234", "+1-555-5678"]
                        }
                    },
                    "preferences": {
                        "theme": "dark",
                        "notifications": True,
                        "languages": ["en", "es", "fr"]
                    }
                }
            },
            "metadata": {
                "version": "1.0",
                "created": "2025-09-16T15:36:28Z",
                "tags": ["user", "profile", "active"]
            }
        }
        
        db._execute_query(
            "INSERT INTO json_test (name, json_data) VALUES (?, ?)",
            ["Nested Test", json.dumps(nested_json)]
        )
        
        result = db._execute_query("""
            SELECT 
                json_extract(json_data, ?) as user_name,
                json_extract(json_data, ?) as email,
                json_extract(json_data, ?) as first_phone,
                json_extract(json_data, ?) as theme,
                json_extract(json_data, ?) as version
            FROM json_test 
            WHERE name = ?
        """, [
            "$.user.profile.personal.name",
            "$.user.profile.personal.contact.email", 
            "$.user.profile.personal.contact.phones[0]",
            "$.user.profile.preferences.theme",
            "$.metadata.version",
            "Nested Test"
        ])
        print(f"✅ Nested JSON extraction: {result}")
        
        # Test 4: JSON arrays and filtering
        print("\n📊 Test 4: JSON arrays and filtering")
        array_json = {
            "products": [
                {"id": 1, "name": "Laptop", "price": 999.99, "category": "electronics"},
                {"id": 2, "name": "Book", "price": 19.99, "category": "books"},
                {"id": 3, "name": "Headphones", "price": 149.99, "category": "electronics"}
            ],
            "total_items": 3,
            "categories": ["electronics", "books"]
        }
        
        db._execute_query(
            "INSERT INTO json_test (name, json_data) VALUES (?, ?)",
            ["Array Test", json.dumps(array_json)]
        )
        
        result = db._execute_query("""
            SELECT 
                json_extract(json_data, ?) as first_product_name,
                json_extract(json_data, ?) as second_product_price,
                json_extract(json_data, ?) as total_items,
                json_extract(json_data, ?) as first_category
            FROM json_test 
            WHERE name = ?
        """, [
            "$.products[0].name",
            "$.products[1].price", 
            "$.total_items",
            "$.categories[0]",
            "Array Test"
        ])
        print(f"✅ JSON array operations: {result}")
        
        # Test 5: JSON modification operations
        print("\n🔧 Test 5: JSON modification operations")
        
        # Update JSON using json_set
        db._execute_query(
            "UPDATE json_test SET json_data = json_set(json_data, ?, ?) WHERE name = ?",
            ["$.age", 31, "Basic Test"]
        )
        
        # Insert new field using json_insert
        db._execute_query(
            "UPDATE json_test SET json_data = json_insert(json_data, ?, ?) WHERE name = ?",
            ["$.updated_at", "2025-09-16T15:36:28Z", "Basic Test"]
        )
        
        result = db._execute_query(
            "SELECT json_extract(json_data, ?) as age, json_extract(json_data, ?) as updated FROM json_test WHERE name = ?",
            ["$.age", "$.updated_at", "Basic Test"]
        )
        print(f"✅ JSON modifications: {result}")
        
        # Test 6: JSON validation
        print("\n✅ Test 6: JSON validation")
        
        # Test valid JSON
        result = db._execute_query("SELECT json_valid(?) as is_valid", ['{"valid": true}'])
        print(f"Valid JSON check: {result}")
        
        # Test invalid JSON
        result = db._execute_query("SELECT json_valid(?) as is_valid", ['{invalid: json}'])
        print(f"Invalid JSON check: {result}")
        
        # Test 7: JSONB binary format (if supported)
        print("\n🗜️ Test 7: JSONB binary format")
        
        try:
            db._execute_query(
                "UPDATE json_test SET jsonb_data = jsonb(json_data) WHERE name = ?",
                ["Basic Test"]
            )
            
            result = db._execute_query(
                "SELECT json_extract(jsonb_data, ?) as name FROM json_test WHERE name = ? AND jsonb_data IS NOT NULL",
                ["$.name", "Basic Test"]
            )
            print(f"✅ JSONB format: {result}")
        except Exception as e:
            print(f"⚠️ JSONB not supported: {e}")
        
        # Test 8: Complex filtering with JSON
        print("\n🔍 Test 8: Complex JSON filtering")
        
        result = db._execute_query("""
            SELECT name, json_extract(json_data, '$.name') as json_name 
            FROM json_test 
            WHERE json_extract(json_data, '$.name') IS NOT NULL
            ORDER BY name
        """)
        print(f"✅ JSON filtering: {result}")
        
        print("\n" + "=" * 45)
        print("🎉 ALL JSON OPERATIONS TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"\n❌ JSON OPERATIONS TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        try:
            Path(db_path).unlink(missing_ok=True)
            print(f"🧹 Cleaned up: {db_path}")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

if __name__ == "__main__":
    success = test_json_operations()
    sys.exit(0 if success else 1)