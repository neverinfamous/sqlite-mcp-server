#!/usr/bin/env python3
"""
Test multi-database support in sqlite-mcp-server
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp_server_sqlite.server import EnhancedEnhancedSqliteDatabase
from mcp_server_sqlite.db_integration import DatabaseIntegration

def test_multi_database():
    """Test creating and using multiple databases in different locations"""
    
    print("🗄️ Testing Multi-Database Support")
    print("=" * 40)
    
    # Test database paths
    db1_path = "./test-db1.db"
    db2_path = "./data/test-db2.db" 
    db3_path = "/tmp/test-db3.db"
    
    # Ensure data directory exists
    Path("./data").mkdir(exist_ok=True)
    
    databases = {}
    
    try:
        # Test 1: Create multiple databases
        print("📁 Test 1: Creating databases in different locations")
        
        for name, path in [("db1", db1_path), ("db2", db2_path), ("db3", db3_path)]:
            print(f"  Creating {name} at {path}")
            db = EnhancedSqliteDatabase(path)
            db = DatabaseIntegration.enhance_database(db)
            databases[name] = db
            
            # Create unique table in each database
            db._execute_query(f"""
                CREATE TABLE {name}_data (
                    id INTEGER PRIMARY KEY,
                    database_name TEXT NOT NULL,
                    data_value INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert test data
            db._execute_query(
                f"INSERT INTO {name}_data (database_name, data_value) VALUES (?, ?)",
                [name, hash(path) % 1000]
            )
            
            print(f"  ✅ {name} created and populated")
        
        # Test 2: Verify data isolation
        print("\n🔒 Test 2: Verify data isolation between databases")
        
        for name, db in databases.items():
            tables = db._execute_query("SELECT name FROM sqlite_master WHERE type='table'")
            table_names = [t['name'] for t in tables]
            print(f"  {name} tables: {table_names}")
            
            data = db._execute_query(f"SELECT * FROM {name}_data")
            print(f"  {name} data: {data}")
        
        # Test 3: Cross-database operations (should be isolated)
        print("\n🚫 Test 3: Verify cross-database isolation")
        
        for name, db in databases.items():
            try:
                # Try to access another database's table (should fail)
                other_tables = [f"{other}_data" for other in databases.keys() if other != name]
                if other_tables:
                    db._execute_query(f"SELECT * FROM {other_tables[0]}")
                    print(f"  ❌ {name} should NOT access {other_tables[0]}")
            except Exception as e:
                print(f"  ✅ {name} correctly isolated: {str(e)[:50]}...")
        
        # Test 4: File system verification
        print("\n📂 Test 4: Verify database files exist")
        
        for name, path in [("db1", db1_path), ("db2", db2_path), ("db3", db3_path)]:
            if Path(path).exists():
                size = Path(path).stat().st_size
                print(f"  ✅ {name} file exists: {path} ({size} bytes)")
            else:
                print(f"  ❌ {name} file missing: {path}")
        
        print("\n" + "=" * 40)
        print("🎉 MULTI-DATABASE TESTS COMPLETED!")
        return True
        
    except Exception as e:
        print(f"\n❌ MULTI-DATABASE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        for path in [db1_path, db2_path, db3_path]:
            try:
                Path(path).unlink(missing_ok=True)
                print(f"🧹 Cleaned up: {path}")
            except Exception as e:
                print(f"⚠️ Cleanup warning for {path}: {e}")

if __name__ == "__main__":
    success = test_multi_database()
    sys.exit(0 if success else 1)