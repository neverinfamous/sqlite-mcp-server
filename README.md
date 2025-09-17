# SQLite MCP Server

*Last Updated September 16, 2025 7:54 PM EST - v1.4.0*

## Overview

The SQLite MCP Server provides advanced database interaction and business intelligence capabilities through SQLite featuring Backup/Restore operations, Full-Text Search (FTS5), enhanced JSONB support for improved JSON storage efficiency, transaction safety for all database operations, foreign key constraint enforcement, enhanced error handling, and detailed diagnostics.

## Key Features

- **JSONB Binary Storage**: Efficient binary JSON storage for improved performance and reduced storage requirements (~15% space savings)
- **Transaction Safety**: All write operations automatically wrapped in transactions with proper rollback on errors
- **Foreign Key Enforcement**: Automatic enforcement of foreign key constraints across all connections
- **Advanced SQL Support**: Complex queries including window functions, subqueries, and advanced filtering
- **Business Intelligence**: Integrated memo resource for capturing business insights during analysis
- **Enhanced Error Handling**: Detailed diagnostics for JSON-related errors with specific suggestions for fixing issues
- **Multi-Level Caching**: Hierarchical caching for optimal performance
- **Pattern Recognition**: Automatic optimization of frequently executed queries
- **JSON Validation**: Prevents invalid JSON from being stored in the database
- **Comprehensive Schema Tools**: Enhanced tools for exploring and documenting database structure
- **Database Administration Tools**: Complete suite of maintenance tools including VACUUM, ANALYZE, integrity checks, performance statistics, and index usage analysis
- **Full-Text Search (FTS5)**: Comprehensive FTS5 implementation with table creation, index management, and enhanced search with BM25 ranking and snippets
- **Backup/Restore Operations**: Enterprise-grade backup and restore capabilities with SQLite backup API, integrity verification, and safety confirmations
- **Advanced SQLite Engine**: Upgraded to SQLite 3.45.x with significant performance enhancements

## Attribution

This project is based on the original SQLite MCP Server from the [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers/tree/2025.4.24/src/sqlite) repository. We extend our sincere gratitude to the original developers and the Model Context Protocol team for creating the foundational server that made this enhanced version possible.

**Original Authors**: Model Context Protocol Team  
**Original Repository**: https://github.com/modelcontextprotocol/servers  
**License**: MIT License

This enhanced version builds upon their excellent foundation with additional features including:
- Enhanced JSONB binary storage support
- Advanced transaction safety mechanisms  
- Comprehensive parameter binding
- Multi-database configuration support
- Full-Text Search (FTS5)
- Backup/Restore Operations
- Database Administration Tools
- Extended error handling and diagnostics
- Production-ready Docker containerization
- Comprehensive testing and validation

## Using Full-Text Search

The SQLite MCP Server provides comprehensive full-text search capabilities through its integrated FTS5 extension with dedicated management tools.

### FTS5 Management Tools

**Create FTS5 Tables:**
```javascript
create_fts_table({
  "table_name": "documents_fts",
  "columns": ["title", "content", "category"],
  "content_table": "documents",  // Optional: populate from existing table
  "tokenizer": "unicode61"       // Optional: unicode61, porter, ascii
})
```

**Enhanced Search with Ranking:**
```javascript
fts_search({
  "table_name": "documents_fts",
  "query": "database optimization",
  "limit": 10,
  "snippet_length": 50
})
// Returns: BM25 ranking, highlighted snippets, structured results
```

**Rebuild Indexes for Performance:**
```javascript
rebuild_fts_index({
  "table_name": "documents_fts"
})
```

### Manual Search Examples

```javascript
// Basic full-text search
read_query({
  "query": "SELECT * FROM documents_fts WHERE documents_fts MATCH 'integration' LIMIT 10"
})

// Phrase search with exact matching
read_query({
  "query": "SELECT * FROM documents_fts WHERE documents_fts MATCH '\"exact phrase\"'"
})
```

### Search Best Practices

- Use double quotes for exact phrase matching: `"exact phrase"`
- Use asterisk for prefix matching: `integrat*` (matches "integration", "integrate", etc.)
- Combine terms with AND/OR: `database AND design`, `sqlite OR mysql`
- Use the rank ordering for most relevant results first

### Advanced Search Techniques

The FTS5 extension supports advanced search techniques:

- **Phrase matching**: `"thread management"`
- **Boolean operators**: `cloudflare AND workers`
- **Prefix matching**: `cloud*`
- **Exclusion**: `NOT redis`
- **Combinations**: `"pattern analysis" NOT quantum`

For programmatic access, use the SQLite FTS5 interface with snippet highlighting:

```sql
-- Search with result highlighting
SELECT 
  id, title, 
  snippet(documents_fts, 0, '<em>', '</em>', '...', 15) AS snippet
FROM 
  documents_fts
WHERE 
  documents_fts MATCH 'search term'
ORDER BY 
  rank
LIMIT 10;
```

## Backup & Restore Operations

The SQLite MCP Server provides enterprise-grade backup and restore capabilities using SQLite's native backup API for atomic, consistent operations.

### Backup Operations

**Create Database Backups:**
```javascript
backup_database({
  "backup_path": "./backups/database_2025-09-16.db",
  "overwrite": false  // Optional: prevent accidental overwrites
})
```

**Verify Backup Integrity:**
```javascript
verify_backup({
  "backup_path": "./backups/database_2025-09-16.db"
})
// Returns: file size, integrity check, table count, version info
```

### Restore Operations

**Restore from Backup:**
```javascript
restore_database({
  "backup_path": "./backups/database_2025-09-16.db",
  "confirm": true  // Required for safety
})
```

### Safety Features

- **Confirmation Required**: All restore operations require explicit `confirm=true`
- **Pre-restore Backup**: Current database automatically backed up before restore
- **Integrity Verification**: Comprehensive backup validation before operations
- **Atomic Operations**: Uses SQLite backup API for consistent, reliable operations
- **Directory Creation**: Automatically creates backup directories as needed

## Components

### Resources

The server exposes dynamic resources:

- **`memo://insights`**: A continuously updated business insights memo
  - Auto-updates as new insights are discovered via the `append_insight` tool
  - Provides a living document of analytical findings
  - Integrates with all analysis workflows

- **`diagnostics://json`**: JSON capabilities diagnostic information
  - Provides information about SQLite JSONB support
  - Shows schema status and optimization recommendations

### Tools

#### Query Tools

- **`read_query`**: Execute SELECT queries with support for window functions and parameter binding
  ```javascript
  read_query({
    "query": "SELECT name, value, RANK() OVER(ORDER BY value DESC) as rank FROM table_name"
  })
  
  // With parameter binding (recommended for dynamic queries)
  read_query({
    "query": "SELECT * FROM table_name WHERE category = ? AND value > ?",
    "params": ["electronics", 100]
  })
  ```

- **`write_query`**: Execute INSERT, UPDATE, or DELETE queries with transaction safety and parameter binding
  ```javascript
  write_query({
    "query": "INSERT INTO table_name (name, value) VALUES ('Item A', 100), ('Item B', 200)"
  })
  
  // With parameter binding (prevents SQL injection)
  write_query({
    "query": "INSERT INTO table_name (name, value) VALUES (?, ?)",
    "params": ["Item C", 300]
  })
  ```

- **`create_table`**: Create new tables in the database
  ```javascript
  create_table({
    "query": "CREATE TABLE table_name (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)"
  })
  ```

#### Schema Tools

- **`list_tables`**: Get a list of all tables in the database
  ```javascript
  list_tables()
  ```

- **`describe_table`**: Show schema information for a specific table
  ```javascript
  describe_table({
    "table_name": "table_name"
  })
  ```

#### Analysis Tools

- **`append_insight`**: Add a business insight to the memo resource
  ```javascript
  append_insight({
    "insight": "Item C has the highest value at 300, which is 50% above the average of all items."
  })
  ```

#### Diagnostic Tools

- **`validate_json`**: Validate JSON string and provide detailed feedback
  ```javascript
  validate_json({
    "json_str": '{"key": "value", "array": [1, 2, 3]}'
  })
  ```

## Major Enhancements

### 1. JSONB Binary Storage

The SQLite MCP Server implements SQLite 3.45's JSONB binary storage format for all JSON data, providing significant advantages:

- **Reduced Storage Size**: 15% space savings across migrated tables
- **Faster Parsing**: No need to re-parse JSON text for each operation
- **Type Preservation**: Binary format preserves data types without text conversion
- **Elimination of Escaping Issues**: No complex character escaping needed
- **Efficient Path Access**: Optimized for JSON path extraction operations

#### Usage:

For optimal JSON handling, SQLite automatically uses JSONB format internally. Simply provide JSON strings directly:

```javascript
// Insert JSON record directly (automatically uses JSONB internally)
write_query({
  "query": "INSERT INTO table_name (json_column) VALUES ('{"key": "value"}')"
})

// With parameter binding (for programmatic access)
write_query({
  "query": "INSERT INTO table_name (json_column) VALUES (?)",
  "params": [JSON.stringify({"key": "value"})]
})

// Query using standard JSON functions
read_query({
  "query": "SELECT json_extract(json_column, '$.key') FROM table_name"
})
```

Note: The explicit `jsonb()` function should only be used in specific advanced cases or when required for parameter binding pattern. For direct SQL statements, standard JSON strings work efficiently.

### 2. Transaction Safety

All write operations are now automatically wrapped in transactions with proper rollback on error:

- **Explicit Transaction Wrapping**: All write operations (INSERT, UPDATE, DELETE) are automatically wrapped in BEGIN/COMMIT transactions
- **Automatic Rollback**: If an operation fails or is interrupted, changes are automatically rolled back to prevent partial writes
- **Selective Application**: Only applies to write operations, leaving read operations unchanged for performance
- **WAL Mode Compatible**: Works alongside the existing Write-Ahead Logging (WAL) journal mode

#### Benefits:

- **Reduced Corruption Risk**: Protects against database corruption due to interrupted operations
- **Data Consistency**: Ensures all-or-nothing operations with no partial updates
- **Error Recovery**: Automatically rolls back failed operations
- **Thread Length Protection**: Mitigates risks associated with conversation length limits
- **Message Interruption Protection**: Handles cases where operations are cut off mid-execution

### 3. Foreign Key Constraint Enforcement

The server now automatically enables foreign key constraints for all database connections:

- **Automatic Enforcement**: Foreign keys are enabled for every connection
- **Consistent Behavior**: All operations respect foreign key constraints
- **Improved Data Integrity**: Prevents orphaned records and maintains referential integrity
- **Special Query Handling**: Proper handling of PRAGMA foreign_keys queries

## Best Practices for Using SQLite MCP

### Standard Query Workflow

1. Start with `list_tables` to identify available tables
   ```javascript
   list_tables()
   ```

2. For each relevant table, use `describe_table` to verify exact schema
   ```javascript
   describe_table({"table_name": "users"})
   ```

3. Based on verified schema, construct appropriate queries using exact column names
   ```javascript
   read_query({
     "query": "SELECT id, name, email FROM users WHERE status = 'active' ORDER BY created_at DESC LIMIT 5"
   })
   ```

4. When searching for specific content, use LIKE with wildcards (%) to increase match probability
   ```javascript
   read_query({
     "query": "SELECT id, project_type, description FROM projects WHERE description LIKE '%keyword%' ORDER BY last_updated DESC LIMIT 5"
   })
   ```

5. For JSON operations, use standard JSON strings for both direct queries and parameter binding
   ```javascript
   // Direct SQL with JSON string
   write_query({
     "query": "INSERT INTO table_name (json_data) VALUES ('{"key": "value"}')"
   })
   
   // With parameter binding
   write_query({
     "query": "INSERT INTO table_name (json_data) VALUES (?)",
     "params": [JSON.stringify({"key": "value"})]
   })
   ```

### Example JSON Operations

```javascript
// Insert JSON record with parameter binding (recommended)
write_query({
  "query": "INSERT INTO products (name, details, metadata) VALUES (?, ?, ?)",
  "params": ["Product A", "High-quality item", "{\"category\": \"electronics\", \"tags\": [\"new\", \"popular\"]}"]
})

// Extract value from JSON
read_query({
  "query": "SELECT json_extract(metadata, '$.tags[0]') FROM products WHERE name = ?",
  "params": ["Product A"]
})

// Update nested JSON value with parameters
write_query({
  "query": "UPDATE products SET metadata = json_set(metadata, '$.category', ?) WHERE id = ?",
  "params": ["updated_category", 123]
})

// Filter by JSON value with parameters
read_query({
  "query": "SELECT id, name FROM products WHERE json_extract(metadata, '$.category') = ?",
  "params": ["electronics"]
})
```

### SQLite-Specific Query Structure

- **Use SQLite-style PRIMARY KEY**: `INTEGER PRIMARY KEY` not `AUTO_INCREMENT`
- **Use TEXT for strings**: SQLite uses `TEXT` instead of `VARCHAR`
- **JSON storage is automatic**: Direct JSON strings are automatically stored efficiently
- **Use proper date functions**: SQLite date functions differ from MySQL
- **No enum type**: Use CHECK constraints instead of ENUM
- **No LIMIT with OFFSET**: Use `LIMIT x OFFSET y` syntax

### Correct Tool Usage Examples

#### SQLite Example

```javascript
// Get table list from SQLite
list_tables()

// Query data from SQLite
read_query({
  "query": "SELECT * FROM users LIMIT 5"
})

// Query with parameters (recommended for dynamic queries)
read_query({
  "query": "SELECT * FROM users WHERE status = ? LIMIT ?",
  "params": ["active", 5]
})

// Update data in SQLite with parameter binding (recommended)
write_query({
  "query": "UPDATE products SET metadata = ? WHERE id = ?",
  "params": ["{\"key\": \"value\"}", 123]
})

// Insert with multiple parameters
write_query({
  "query": "INSERT INTO users (name, email, status) VALUES (?, ?, ?)",
  "params": ["John Doe", "john@example.com", "active"]
})

// Get table structure in SQLite
describe_table({
  "table_name": "users"
})
```

#### MySQL Example

```javascript
// Get table list from MySQL
list_tables()

// Query data from MySQL
query({
  "sql": "SELECT * FROM users LIMIT 5"
})

// Update data in MySQL
execute({
  "sql": "UPDATE users SET status = 'active' WHERE id = 123"
})

// Get table structure in MySQL
describe_table({
  "table": "users"
})
```

## Troubleshooting

### System Status

**Last Comprehensive Test**: September 16, 2025 - All core database operations, JSONB support, transaction safety, and business intelligence features verified functional.

### JSONB-Specific Troubleshooting

If you encounter JSON-related errors:

1. **"no such function: jsonb"**: Your SQLite version doesn't support JSONB (requires 3.45.0+)
   ```javascript
   // Check SQLite version
   read_query({"query": "SELECT sqlite_version()"})
   ```

2. **"Invalid JSON in column"**: The JSON string is malformed
   ```javascript
   // Validate JSON first
   validate_json({"json_str": jsonString})
   ```

3. **"JSON parse error"**: JSON syntax is incorrect
   ```javascript
   // Use correct JSON format with double quotes
   // Incorrect: {'key': 'value'}
   // Correct: {"key": "value"}
   ```

### Transaction Safety Troubleshooting

1. **"database is locked"**: Another connection is holding the database lock
   - This error should be less common with transaction safety, but can still occur
   - Check for long-running transactions in other processes
   
2. **"Error during rollback"**: Problem occurred during transaction rollback
   - Check the database integrity
   - Restart the MCP server if persistent

### Foreign Key Troubleshooting

1. **"foreign key constraint failed"**: Attempted to violate a foreign key constraint
   - Verify the referenced record exists before inserting/updating
   - Use proper cascading delete where appropriate
   
2. **"PRAGMA foreign_keys error"**: Problem enabling foreign keys
   - This should not occur with the enhanced implementation
   - Check if using a compatible SQLite version

### Additional Troubleshooting Areas

1. **Database connectivity issues**:
   - Check file paths and permissions
   - Ensure SQLite database file is accessible
   - Verify database file is not corrupted

2. **Performance issues**:
   - Check database size and indexes
   - Consider running VACUUM for optimization
   - Review query complexity

3. **JSON data issues**:
   - Validate JSON strings before insertion
   - Use parameter binding for complex JSON data
   - Check for proper escaping in JSON strings

## Database Maintenance

The SQLite MCP Server includes basic database maintenance capabilities:

- **Integrity Checks**: Basic SQLite PRAGMA integrity_check support
- **JSON Validation**: Automatic validation of JSON data during INSERT/UPDATE operations
- **Transaction Safety**: Automatic rollback on errors to prevent data corruption

## Database Configuration

The SQLite MCP Server supports flexible database configuration to work with any SQLite database file:

### Quick Start Options

```bash
# Use project root with auto-detection
python start_sqlite_mcp.py

# Create data directory structure  
python start_sqlite_mcp.py --create-data-dir

# Use specific database file
python start_sqlite_mcp.py --db-path /path/to/your/database.db

# Use in-memory database (testing)
python start_sqlite_mcp.py --db-path :memory:
```

### MCP Client Configuration

```json
{
  "mcpServers": {
    "sqlite-local": {
      "command": "python",
      "args": [
        "/path/to/sqlite-mcp-server/start_sqlite_mcp.py",
        "--db-path", "/path/to/your/database.db"
      ]
    }
  }
}
```

The server automatically detects project structure and creates appropriate database locations, supporting both relative and absolute paths for maximum flexibility.

## Production Status ✅

**Current Status**: **PRODUCTION READY** - Comprehensive system testing completed September 16, 2025

### System Test Results
- ✅ **Core Functionality**: All database operations (SELECT, INSERT, UPDATE, DELETE, CREATE, DROP) verified working
- ✅ **JSONB Support**: Binary JSON storage and json_extract() functions confirmed functional  
- ✅ **Transaction Safety**: Write operations completing successfully with proper rollback
- ✅ **Schema Operations**: Table listing, schema inspection, and describe_table operations working
- ✅ **Advanced Features**: Memo/insights functionality, maintenance logging, and integrity monitoring active
- ✅ **Parameter Binding**: Enhanced support for parameterized queries with ? placeholders
- ✅ **Multi-Database Support**: Flexible database path configuration for any SQLite file
- ✅ **Advanced FTS5 search**: All FTS5 capabilities confirmed working
- ✅ **Database Administration Tools**: Analyze, integrity check, database_stats, index_usage_stats and vacuum confirmed working
- ✅ **Maintenance Systems**: Basic integrity checks and database optimization confirmed working

### Known Minor Issues (Non-Critical)
- **JSON Formatting**: Standard JSON formatting resolves any escaping issues
- **Complex Queries**: Advanced parameterized queries supported with proper parameter binding

## Installation Requirements

### Core Requirements (Required)
- **Python 3.10+**: Programming language runtime
- **SQLite 3.45.0+**: Core database engine with JSONB support (current system: 3.50.2)
- **MCP 1.14.0+**: Model Context Protocol library

### Optional JavaScript Utilities (Advanced Users Only)
- **Node.js 18+**: For optional JavaScript JSONB utilities (fully reconstructed and ESLint compliant)
- **Visual Studio C++ Build Tools**: Required only if using JavaScript utilities with better-sqlite3
- **Note**: The main MCP server is Python-based and works perfectly without any JavaScript dependencies

**For most users**: You only need Python requirements. The JavaScript utilities are optional helpers for advanced use cases.

## JSON Validation and JSONB Support

### JSON Validation System

The SQLite MCP Server includes comprehensive JSON validation capabilities:

1. **Automatic JSON Field Validation**:
   - Validates formatting across all JSON fields in 32 columns
   - Ensures valid JSON structure during operations
   - Reports malformed JSON through notifications

2. **Validation Triggers**:
   - Automatically created SQLite triggers for INSERT/UPDATE operations
   - Prevents invalid JSON from being inserted or updated
   - Covers 16 tables with JSON/JSONB columns

3. **Repair Capabilities**:
   - Attempts to repair malformed JSON when found
   - Preserves as much data as possible during repairs
   - Records repair attempts in maintenance logs

### JSONB Binary Storage Migration

All JSON columns have been migrated to the JSONB binary storage format, providing:

- Improved storage efficiency (~15% smaller)
- Better query performance for JSON operations
- Enhanced validation during data changes
- Improved type preservation

The migration to JSONB is transparent to users - simply continue using standard JSON operations as shown in the examples.

## Planned Future Enhancements

#### **1. Virtual Table Management - MEDIUM PRIORITY**
- **Missing**: Tools to create/manage virtual tables beyond FTS5
- **Examples**: CSV virtual tables, memory virtual tables

#### **2. Advanced PRAGMA Operations - MEDIUM PRIORITY**
- **Missing**: Comprehensive PRAGMA management tools
- **Current**: Can execute PRAGMA via queries, but no specialized tools

#### **3. R-Tree Index Support - LOW PRIORITY**
- **Missing**: Spatial indexing for geometric data
- **Current**: No specialized tools for R-Tree operations

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Security

If you discover a security vulnerability, please follow our [Security Policy](SECURITY.md) for responsible disclosure.

## Support

- 📝 [Open an issue](https://github.com/neverinfamous/mcp_server_sqlite/issues) for bug reports or feature requests
- 🌐 Visit memory-journal-mcp (https://github.com/neverinfamous/memory-journal-mcp)

## Resources

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLite JSON1 Extension](https://www.sqlite.org/json1.html)
- [SQLite JSONB Support](https://www.sqlite.org/draft/releaselog/3_45_0.html)
- [better-sqlite3 Documentation](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md)
- [MCP Protocol Specification](https://mcp-protocol.org/specification)
- [SQL Window Functions Tutorial](https://www.sqlitetutorial.net/sqlite-window-functions/)

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.