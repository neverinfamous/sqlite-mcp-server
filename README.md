# SQLite MCP Server

*Last Updated September 16, 2025 12:50 PM EST *

## Overview

The SQLite MCP Server provides advanced database interaction and business intelligence capabilities through SQLite featuring enhanced JSONB support for improved JSON storage efficiency, transaction safety for all database operations, foreign key constraint enforcement, enhanced error handling, and detailed diagnostics.

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
- **Advanced SQLite Engine**: Upgraded to SQLite 3.45.x with significant performance enhancements

## Using Full-Text Search

The SQLite MCP Server provides powerful full-text search capabilities through its integrated FTS5 extension. This allows for efficient and accurate searching across all database content.

### Search Examples

```javascript
// Basic full-text search across memory journal entries
read_query({
  "query": "SELECT id, entry_type, content FROM memory_journal_fts WHERE memory_journal_fts MATCH 'integration' LIMIT 10"
})

// Search with ranking by relevance
read_query({
  "query": "SELECT id, entry_type, content, rank FROM memory_journal_fts WHERE memory_journal_fts MATCH 'database design' ORDER BY rank LIMIT 5"
})

// Phrase search with exact matching
read_query({
  "query": "SELECT id, entry_type FROM memory_journal_fts WHERE memory_journal_fts MATCH '\"lite integration\"'"
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
  id, entry_type, 
  snippet(memory_journal_fts, 0, '<em>', '</em>', '...', 15) AS snippet
FROM 
  memory_journal_fts
WHERE 
  memory_journal_fts MATCH 'search term'
ORDER BY 
  rank
LIMIT 10;
```

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
   describe_table({"table_name": "memory_journal"})
   ```

3. Based on verified schema, construct appropriate queries using exact column names
   ```javascript
   read_query({
     "query": "SELECT id, entry_type, content FROM memory_journal WHERE entry_type = 'identity_statement' ORDER BY timestamp DESC LIMIT 5"
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
  "query": "INSERT INTO memory_journal (entry_type, content, metadata) VALUES (?, ?, ?)",
  "params": ["test_entry", "Test content", "{\"key\": \"value\", \"array\": [1, 2, 3]}"]
})

// Extract value from JSON
read_query({
  "query": "SELECT json_extract(metadata, '$.array[1]') FROM memory_journal WHERE entry_type = ?",
  "params": ["test_entry"]
})

// Update nested JSON value with parameters
write_query({
  "query": "UPDATE memory_journal SET metadata = json_set(metadata, '$.key', ?) WHERE id = ?",
  "params": ["new_value", 123]
})

// Filter by JSON value with parameters
read_query({
  "query": "SELECT id, content FROM memory_journal WHERE json_extract(metadata, '$.key') = ?",
  "params": ["value"]
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
  "query": "SELECT * FROM repositories LIMIT 5"
})

// Query with parameters (recommended for dynamic queries)
read_query({
  "query": "SELECT * FROM repositories WHERE status = ? LIMIT ?",
  "params": ["active", 5]
})

// Update data in SQLite with parameter binding (recommended)
write_query({
  "query": "UPDATE memory_journal SET metadata = ? WHERE id = ?",
  "params": ["{\"key\": \"value\"}", 123]
})

// Insert with multiple parameters
write_query({
  "query": "INSERT INTO repositories (name, url, status) VALUES (?, ?, ?)",
  "params": ["my-repo", "https://github.com/user/repo", "active"]
})

// Get table structure in SQLite
describe_table({
  "table_name": "repositories"
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

**Last Comprehensive Test**: September 16, 2025 - All core systems verified functional with 67 tables, 1,996 entries, active monitoring, and maintenance systems operational.

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

1. **Schema documentation issues**:
   - Check file paths in configuration
   - Ensure proper permissions to write files
   - Verify SQLite database is accessible

2. **Thread verification issues**:
   - Check database integrity first
   - Repair orphaned threads with appropriate tools
   - Review thread_map table for inconsistencies

3. **GitHub API rate limiting**:
   - Use authenticated requests consistently
   - Consider caching GitHub responses

4. **Token expiration**:
   - Update the GitHub token in the configuration
   - Verify token permissions include repo access

5. **False positives for unregistered repositories**:
   - Update exclusion patterns in configuration
   - Manually mark repositories to exclude

### Log Files

Check these log files for troubleshooting:

- Database maintenance logs
- Thread initialization logs
- Repository verification logs
- Schema extraction logs
- Documentation generation logs

## Maintenance and Repair Capabilities

### Database Maintenance and Verification

The SQLite MCP Server includes comprehensive database maintenance capabilities:

- **Integrity Checks**: Validates database structure, foreign keys, and data consistency
- **Schema Tracking**: Monitors and documents database schema evolution over time 
- **Repository Verification**: Ensures consistency between database records and both local and GitHub repositories
- **Thread Management**: Verifies thread continuity and maintains thread relationships
- **Repository Relationship Analysis**: Monitors relationships between repositories
- **Notification System**: Alerts about issues with appropriate severity levels

#### Database Integrity Checks

- **Structural Integrity**: Verifies database structure against expected schema
- **Foreign Key Constraints**: Ensures all foreign key relationships are valid
- **Index Validation**: Checks that all indexes are properly maintained
- **Orphaned Records**: Identifies and resolves orphaned records
- **Database Optimization**: Performs VACUUM and other optimization tasks
- **Performance Analysis**: Analyzes query performance and suggests optimizations

#### Repository Registry Verification

- **Local Repository Checks**: Verifies repository local paths exist and are valid Git repositories
- **GitHub Integration**: Validates GitHub repository status using the GitHub API
- **Unregistered Repository Detection**: Identifies local Git repositories not yet registered in the database

### Automated Repair Capabilities

The system can automatically repair common issues:

| Issue Type | Repair Strategy |
|------------|-----------------|
| **Database Integrity Issues** |
| Foreign key violations | Update references to valid values or NULL |
| Orphaned records | Remove or update to maintain referential integrity |
| Corrupted JSON fields | Reformat or reset to valid JSON |
| **Repository Issues** |
| Missing local path | Re-clone from GitHub if URL exists, otherwise mark as deleted |
| Not Git repository | Re-clone from GitHub to restore Git directory |
| GitHub repository missing | Mark repository as deleted in database |
| Unregistered repository | Add repository to the registry with detected information |
| **Thread Map Issues** |
| Orphaned threads | Connect to appropriate parent or mark as root thread |
| Duplicate thread entries | Remove duplicates, keeping the most complete entry |
| Invalid references | Repair references to valid repository IDs |
| **Schema Issues** |
| Schema extraction failures | Reset extraction state and retry with different options |
| Git hook configuration | Repair or reinstall Git hooks |

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

## Future Enhancements

Planned improvements to the SQLite MCP Server include:

1. **Enhanced Duplicate Detection**: More robust checks to prevent duplicate entries during registration

2. **Schema Difference Visualization**: Enhanced visual diffs between schema versions

3. **Schema Validation**: Validation of schema against coding standards and best practices

4. **Full-Text Search Optimizations**:
   - Phrase-based ranking improvements
   - Custom tokenizers for technical terms
   - Faceted search capabilities
   - Search result caching

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
- ✅ **Maintenance Systems**: 37 active notifications, integrity checks, and automated monitoring confirmed working

### Known Minor Issues (Non-Critical)
- **Historical Foreign Key Violations**: 71 catalogued foreign key issues from historical data (system functional, data integrity tracking active)
- **JSON Formatting**: Standard JSON formatting resolves any escaping issues
- **Legacy Parameter Binding**: Complex parameterized queries work with new parameter array support

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

## Resources

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLite JSON1 Extension](https://www.sqlite.org/json1.html)
- [SQLite JSONB Support](https://www.sqlite.org/draft/releaselog/3_45_0.html)
- [better-sqlite3 Documentation](https://github.com/JoshuaWise/better-sqlite3/blob/master/docs/api.md)
- [MCP Protocol Specification](https://mcp-protocol.org/specification)
- [SQL Window Functions Tutorial](https://www.sqlitetutorial.net/sqlite-window-functions/)

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

## Schema Documentation System

The SQLite MCP Server includes a comprehensive documentation system for database structure:

### Generated Documentation Files

The documentation system maintains three primary types of documentation:

1. **Schema Documentation**:
   - Complete SQL schema with create statements
   - Detailed table descriptions and column information
   - Foreign key relationship diagrams

2. **ER Diagrams**:
   - Entity-relationship diagrams in Mermaid format
   - Visual representation of database structure

3. **Database Statistics**:
   - Overall database metrics and table statistics
   - Row counts and growth trends

## Notification System

The SQLite MCP Server includes a notification system for alerting about database issues:

### Notification Types

- `database_integrity_issue`: Database integrity check failures
- `thread_map_inconsistency`: Thread map inconsistencies
- `json_validation_error`: JSON validation failures
- `repository_missing`: Repository path not found
- `repository_not_git`: Path exists but is not a Git repository
- `repository_github_mismatch`: GitHub repository not found
- `repository_unregistered`: Git repository exists but is not registered

### Severity Levels

- `critical`: Requires immediate attention
- `high`: Should be addressed soon
- `info`: Informational, no immediate action required

### Managing Notifications

View active notifications:
```sql
SELECT * FROM mike_notifications WHERE seen = 0 ORDER BY severity, created_at DESC;
```

Mark notifications as seen:
```sql
UPDATE mike_notifications SET seen = 1, seen_at = datetime('now') 
WHERE notification_type = 'type_name';
```

Clear all notifications for a repository:
```sql
UPDATE mike_notifications SET seen = 1, seen_at = datetime('now') 
WHERE content LIKE '%repository-name%';
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Security

If you discover a security vulnerability, please follow our [Security Policy](SECURITY.md) for responsible disclosure.

## Support

- 📝 [Open an issue](https://github.com/neverinfamous/mcp_server_sqlite/issues) for bug reports or feature requests
- 💝 [Sponsor this project](https://github.com/sponsors/neverinfamous) to support development
- 🌐 Visit [adamic.tech](https://adamic.tech) for more projects

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.