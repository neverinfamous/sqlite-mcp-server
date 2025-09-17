# SQLite MCP Server

*Last Updated September 17, 2025 2:35 AM EST - v2.0.0*

## Overview

The SQLite MCP Server provides advanced database interaction and business intelligence capabilities featuring **SpatiaLite Geospatial Analytics**, Enhanced Virtual Tables with Smart Type Inference, Vector Index Optimization with ANN search, Intelligent MCP Resources and Prompts, Semantic/Vector Search, Virtual Table Management, Advanced PRAGMA Operations, Backup/Restore operations, Full-Text Search (FTS5), enhanced JSONB support for improved JSON storage efficiency, transaction safety for all database operations, foreign key constraint enforcement, enhanced error handling, and detailed diagnostics.

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
- **Advanced PRAGMA Operations**: Comprehensive SQLite configuration management, performance optimization, and database introspection tools
- **Virtual Table Management**: Complete virtual table lifecycle management for R-Tree spatial indexing, CSV file access, and sequence generation
- **SpatiaLite Geospatial Analytics**: Enterprise-grade GIS capabilities with spatial indexing, geometric operations, and comprehensive spatial analysis
- **Enhanced Virtual Tables**: Smart CSV/JSON import with automatic data type inference, nested object flattening, and schema analysis
- **Semantic/Vector Search**: AI-native semantic search with embedding storage, cosine similarity, and hybrid keyword+semantic ranking
- **Vector Index Optimization**: Approximate Nearest Neighbor (ANN) search with k-means clustering and spatial indexing for sub-linear O(log n) performance
- **Intelligent MCP Resources**: Dynamic database meta-awareness with real-time schema, capabilities, statistics, search indexes, and performance insights
- **Guided MCP Prompts**: Intelligent workflow automation with semantic query translation, table summarization, database optimization, and hybrid search recipes
- **Advanced SQLite Engine**: Upgraded to SQLite 3.50.4 with significant performance enhancements

## Attribution

This project is based on the original SQLite MCP Server from the [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers/tree/2025.4.24/src/sqlite) repository. We extend our sincere gratitude to the original developers and the Model Context Protocol team for creating the foundational server that made this enhanced version possible.

**Original Authors**: Model Context Protocol Team  
**Original Repository**: https://github.com/modelcontextprotocol/servers  
**License**: MIT License

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

## Advanced PRAGMA Operations

The SQLite MCP Server provides comprehensive PRAGMA management tools for database configuration, optimization, and introspection.

### Configuration Management

**Get/Set PRAGMA Settings:**
```javascript
pragma_settings({
  "pragma_name": "journal_mode"
})
// Returns: PRAGMA journal_mode = delete

pragma_settings({
  "pragma_name": "synchronous", 
  "value": "NORMAL"
})
// Sets and confirms: PRAGMA synchronous = NORMAL
```

### Performance Optimization

**Database Optimization:**
```javascript
pragma_optimize({
  "analysis_limit": 1000  // Optional: limit analysis scope
})
// Runs PRAGMA optimize for query performance improvements
```

### Database Introspection

**Detailed Table Information:**
```javascript
pragma_table_info({
  "table_name": "users",
  "include_foreign_keys": true  // Include FK and index info
})
// Returns: columns, foreign keys, indexes, constraints
```

**Database List:**
```javascript
pragma_database_list()
// Returns: all attached databases with file paths and schemas
```

**SQLite Capabilities:**
```javascript
pragma_compile_options()
// Returns: SQLite version, compile options, feature availability
```

### Supported PRAGMA Commands

- **Configuration**: journal_mode, synchronous, cache_size, temp_store
- **Performance**: optimize, analysis_limit, mmap_size  
- **Security**: foreign_keys, recursive_triggers, secure_delete
- **Debugging**: compile_options, database_list, table_info
- **And many more** - supports all SQLite PRAGMA commands

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

## Database Configuration

The SQLite MCP Server provides flexible database configuration with **automatic database creation** - no manual setup required!

### **🚀 Zero-Configuration Start**
The server automatically creates and manages a persistent SQLite database **because MCP operations require persistent storage** between tool calls:
- **Auto-creates** `sqlite_mcp.db` in your project root if none exists
- **Why create a file?** MCP tool calls need shared, persistent data storage (tables, indexes, etc.)
- **Persists all data** between sessions and MCP tool calls  
- **Works immediately** - no database setup or file creation needed
- **Connects to existing databases** - works with any SQLite file you specify

### Quick Start Options

**Use existing database**:
```bash
python start_sqlite_mcp.py --db-path /path/to/your/database.db
```

**Auto-detect project structure** (default):
```bash
python start_sqlite_mcp.py
# Automatically finds project root and creates sqlite_mcp.db
```

**Create organized data directory**:
```bash
python start_sqlite_mcp.py --create-data-dir
# Creates ./data/sqlite_mcp.db in your project
```

### MCP Client Configuration

**For Cursor/Claude Desktop**:
```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "python",
      "args": [
        "/path/to/sqlite-mcp-server/start_sqlite_mcp.py",
        "--db-path", "/path/to/your/database.db"
      ]
    }
  }
}
```

**For Docker**:
```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/host/project:/workspace",
        "ghcr.io/neverinfamous/sqlite-mcp-server:latest",
        "--db-path", "/workspace/database.db"
      ]
    }
  }
}
```

### Database Location Best Practices

- **`./data/sqlite_mcp.db`** - Recommended for projects (organized, version-control friendly)
- **`./sqlite_mcp.db`** - Simple option for small projects  
- **Existing databases** - Use `--db-path` to connect to any SQLite database
- **`:memory:`** - Temporary database for testing (data not persisted)

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

## Virtual Table Management

The SQLite MCP Server provides comprehensive virtual table management capabilities, supporting multiple virtual table types for specialized data access patterns and performance optimization.

### Virtual Table Management Tools

#### **create_rtree_table** - R-Tree Spatial Indexing
Create R-Tree virtual tables for efficient spatial queries and geometric data indexing.

```python
# Create a 2D spatial index for geographic data
create_rtree_table(
    table_name="locations_spatial",
    dimensions=2,
    coordinate_type="float"
)

# Create a 3D spatial index for volumetric data
create_rtree_table(
    table_name="objects_3d",
    dimensions=3,
    coordinate_type="float"
)
```

**Features:**
- Configurable dimensions (2D, 3D, multi-dimensional)
- Float or integer coordinate types
- Automatic column generation (id, min0, max0, min1, max1, etc.)
- Optimized for range queries and spatial searches

#### **create_csv_table** - CSV File Access
Create virtual tables that directly access CSV files with configurable parsing options.

```python
# Create a virtual table for a CSV file with headers
create_csv_table(
    table_name="sales_data",
    csv_file_path="/path/to/sales.csv",
    has_header=True,
    delimiter=","
)

# Create a virtual table for a TSV file without headers
create_csv_table(
    table_name="log_data",
    csv_file_path="/path/to/logs.tsv",
    has_header=False,
    delimiter="\t"
)
```

**Features:**
- Direct CSV file access without importing
- Configurable delimiters (comma, tab, pipe, etc.)
- Header row detection and handling
- Automatic fallback to temporary table if CSV extension unavailable

#### **create_series_table** - Sequence Generation
Create virtual tables that generate numeric sequences for testing, reporting, and data generation.

```python
# Create a simple number series
create_series_table(
    table_name="numbers_1_to_100",
    start_value=1,
    end_value=100,
    step=1
)

# Create a series with custom step
create_series_table(
    table_name="even_numbers",
    start_value=2,
    end_value=1000,
    step=2
)
```

**Features:**
- Configurable start, end, and step values
- Automatic fallback to regular table with recursive CTE
- Perfect for generating test data and sequences
- Memory-efficient virtual table implementation

#### **list_virtual_tables** - Virtual Table Discovery
List all virtual tables in the database with detailed type information.

```python
list_virtual_tables()
```

**Returns:**
- Virtual table names and SQL definitions
- Automatic type detection (rtree, fts, csv, generate_series)
- Complete virtual table inventory
- Structured JSON output with metadata

#### **virtual_table_info** - Schema Inspection
Get detailed information about specific virtual tables including column schemas and configuration.

```python
virtual_table_info(table_name="locations_spatial")
```

**Features:**
- Complete column information with types and constraints
- Virtual table type identification
- SQL definition display
- Column count and metadata

#### **drop_virtual_table** - Safe Removal
Safely remove virtual tables with confirmation requirements to prevent accidental data loss.

```python
# Safe drop with confirmation
drop_virtual_table(
    table_name="old_spatial_index",
    confirm=True
)
```

**Safety Features:**
- Mandatory confirmation flag to prevent accidents
- Virtual table verification before deletion
- Detailed status reporting
- Error handling for non-existent tables

### Virtual Table Use Cases

**Spatial Data Management:**
- Geographic information systems (GIS)
- Location-based services
- Geometric calculations and range queries
- Spatial indexing for performance optimization

**CSV Data Integration:**
- Direct access to external data files
- ETL processes without data importing
- Real-time file monitoring and analysis
- Legacy system integration

**Sequence Generation:**
- Test data creation
- Report numbering and pagination
- Date/time series generation
- Mathematical sequence analysis

### Performance Benefits

- **R-Tree Tables**: O(log n) spatial queries vs O(n) table scans
- **CSV Tables**: Direct file access without storage duplication
- **Series Tables**: Memory-efficient sequence generation
- **Comprehensive Management**: Centralized virtual table lifecycle control

## Semantic/Vector Search

The SQLite MCP Server provides comprehensive semantic search capabilities, enabling AI-native applications with embedding storage, similarity search, and hybrid keyword+semantic ranking. This makes it perfect for recommendation systems, question-answering, and content discovery.

### Semantic Search Tools

#### **create_embeddings_table** - Optimized Embedding Storage
Create tables specifically designed for storing high-dimensional embedding vectors with associated metadata.

```python
# Create embeddings table for OpenAI embeddings (1536 dimensions)
create_embeddings_table(
    table_name="document_embeddings",
    embedding_dim=1536,
    metadata_columns=["category", "source", "author"]
)

# Create embeddings table for smaller models (384 dimensions)
create_embeddings_table(
    table_name="sentence_embeddings", 
    embedding_dim=384,
    metadata_columns=["topic", "language"]
)
```

**Features:**
- Configurable embedding dimensions (384, 768, 1536, custom)
- JSON-based vector storage for maximum SQLite compatibility
- Automatic indexing for dimension-based queries
- Flexible metadata columns for filtering and context
- Timestamp tracking (created_at, updated_at)

#### **store_embedding** - Vector Storage with Metadata
Store embedding vectors alongside their original content and contextual metadata.

```python
# Store document embedding with metadata
store_embedding(
    table_name="document_embeddings",
    embedding=[0.1, -0.3, 0.8, ...],  # 1536-dimensional vector
    content="Comprehensive guide to machine learning algorithms",
    metadata={
        "category": "AI/ML",
        "source": "research_paper",
        "author": "Dr. Smith"
    }
)
```

**Features:**
- Automatic embedding dimension validation
- Flexible metadata storage as key-value pairs
- Content length tracking and validation
- Comprehensive error handling for invalid vectors

#### **semantic_search** - Cosine Similarity Search
Perform semantic similarity searches using cosine similarity with configurable thresholds and limits.

```python
# Semantic search for similar content
semantic_search(
    table_name="document_embeddings",
    query_embedding=[0.2, -0.1, 0.9, ...],  # Query vector
    limit=10,
    similarity_threshold=0.7
)
```

**Features:**
- Cosine similarity calculations with optimized performance
- Configurable similarity thresholds for quality control
- Ranked results by similarity score
- Dimension matching validation
- Detailed search statistics and metadata

#### **hybrid_search** - Keyword + Semantic Fusion
Combine FTS5 keyword search with semantic similarity for the best of both worlds.

```python
# Hybrid search combining keyword precision with semantic understanding
hybrid_search(
    embeddings_table="document_embeddings",
    fts_table="documents_fts",
    query_text="machine learning algorithms",
    query_embedding=[0.15, -0.25, 0.75, ...],
    keyword_weight=0.3,    # 30% keyword importance
    semantic_weight=0.7,   # 70% semantic importance
    limit=15
)
```

**Features:**
- Configurable weighting between keyword and semantic scores
- BM25 + cosine similarity hybrid ranking
- Automatic score normalization and combination
- Comprehensive search statistics and breakdown
- Perfect for question-answering and content discovery

#### **calculate_similarity** - Direct Vector Comparison
Calculate cosine similarity between any two embedding vectors with detailed mathematical breakdown.

```python
# Direct similarity calculation
calculate_similarity(
    vector1=[1.0, 0.5, -0.3, 0.8],
    vector2=[0.9, 0.6, -0.2, 0.7]
)
```

**Features:**
- Precise cosine similarity calculations
- Detailed mathematical breakdown (dot product, magnitudes)
- Dimension validation and error handling
- Perfect for embedding quality analysis and debugging

#### **batch_similarity_search** - Multiple Vector Queries
Perform similarity searches with multiple query vectors in a single efficient operation.

```python
# Batch search for multiple queries
batch_similarity_search(
    table_name="document_embeddings",
    query_embeddings=[
        [0.1, 0.5, -0.2, 0.8],  # Query 1
        [0.3, -0.1, 0.6, 0.4],  # Query 2
        [0.7, 0.2, -0.4, 0.1]   # Query 3
    ],
    limit=5
)
```

**Features:**
- Efficient batch processing of multiple queries
- Individual result sets for each query vector
- Comprehensive error handling per query
- Perfect for recommendation systems and clustering

### Semantic Search Use Cases

**AI-Native Applications:**
- Question-answering systems with semantic understanding
- Content recommendation based on similarity
- Document clustering and categorization
- Semantic duplicate detection

**Hybrid Search Applications:**
- Enterprise search combining exact keywords with meaning
- E-commerce product discovery with natural language
- Knowledge base search with contextual understanding
- Research paper discovery and citation analysis

**Embedding Integration:**
- OpenAI embeddings (text-embedding-3-small/large)
- Hugging Face sentence transformers
- Custom model embeddings
- Multi-modal embeddings (text, image, audio)

### Performance and Scalability

- **Pure SQLite Implementation**: No external dependencies or binary extensions
- **JSON Storage**: Maximum compatibility across all SQLite deployments
- **Optimized Queries**: Dimension-based indexing for faster searches
- **Batch Operations**: Efficient multiple vector processing
- **Memory Efficient**: Streaming similarity calculations for large datasets

### Integration Examples

**With OpenAI API:**
```python
# 1. Generate embeddings using OpenAI
embeddings = openai.embeddings.create(
    model="text-embedding-3-small",
    input="Your content here"
)

# 2. Store in SQLite MCP Server
store_embedding(
    table_name="openai_embeddings",
    embedding=embeddings.data[0].embedding,
    content="Your content here"
)

# 3. Semantic search
results = semantic_search(
    table_name="openai_embeddings", 
    query_embedding=query_vector
)
```

**With Hugging Face:**
```python
# 1. Generate embeddings locally
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode("Your content").tolist()

# 2. Store and search using SQLite MCP Server
store_embedding(table_name="hf_embeddings", embedding=embedding, content="Your content")
```

## SpatiaLite Geospatial Analytics

The SQLite MCP Server provides enterprise-grade geospatial capabilities through SpatiaLite integration, transforming SQLite into a comprehensive GIS platform for location-based business intelligence and spatial data analysis.

### SpatiaLite Integration

**`load_spatialite`** - Load SpatiaLite extension with automatic detection
```javascript
load_spatialite({
  "force_reload": false  // Force reload if already loaded
})
// Returns: Version information for SpatiaLite, PROJ4, and GEOS libraries
```

**`create_spatial_table`** - Create spatial tables with geometry columns
```javascript
create_spatial_table({
  "table_name": "locations",
  "geometry_type": "POINT",           // POINT, LINESTRING, POLYGON, etc.
  "geometry_column": "geom",          // Name of geometry column
  "srid": 4326,                       // Spatial Reference System (WGS84)
  "additional_columns": [             // Additional non-spatial columns
    {"name": "name", "type": "TEXT"},
    {"name": "category", "type": "TEXT"}
  ]
})
```

### Spatial Indexing & Performance

**`spatial_index`** - Manage spatial indexes for high-performance queries
```javascript
spatial_index({
  "table_name": "locations",
  "geometry_column": "geom",
  "action": "create"                  // create or drop
})
```

**Performance Benefits:**
- **Sub-linear query performance** for spatial operations
- **Automatic R-Tree indexing** for geometry columns  
- **Optimized spatial joins** and proximity searches
- **Enterprise-scale** geospatial data handling

### Geometric Operations

**`geometry_operations`** - Common geometric calculations and transformations
```javascript
geometry_operations({
  "operation": "distance",            // buffer, intersection, union, distance, area, etc.
  "geometry1": "POINT(0 0)",         // First geometry (WKT format)
  "geometry2": "POINT(3 4)",         // Second geometry for binary operations
  "buffer_distance": 100.0           // Distance for buffer operations
})
// Returns: Calculated result (e.g., distance: 5.0)
```

**Supported Operations:**
- **Buffer**: Create buffer zones around geometries
- **Distance**: Calculate distances between geometries
- **Area/Length**: Measure geometric properties
- **Intersection/Union**: Geometric set operations
- **Centroid/Envelope**: Geometric transformations

### Advanced Spatial Analysis

**`spatial_analysis`** - Enterprise spatial analysis algorithms
```javascript
spatial_analysis({
  "analysis_type": "nearest_neighbor", // nearest_neighbor, spatial_join, point_in_polygon, etc.
  "source_table": "stores",
  "target_table": "customers",
  "max_distance": 1000.0,             // Maximum distance for proximity operations
  "limit": 100                        // Limit results for performance
})
```

**Analysis Types:**
- **Nearest Neighbor**: Find closest features
- **Spatial Join**: Join tables based on spatial relationships
- **Point-in-Polygon**: Determine containment relationships
- **Distance Matrix**: Calculate all pairwise distances
- **Cluster Analysis**: Spatial clustering with DBSCAN

### Shapefile Integration

**`import_shapefile`** - Import industry-standard Shapefile data
```javascript
import_shapefile({
  "shapefile_path": "/path/to/data.shp",
  "table_name": "imported_features",
  "encoding": "UTF-8",                // Character encoding
  "srid": 4326                        // Override SRID if needed
})
// Returns: Number of features imported
```

### Spatial Queries

**`spatial_query`** - Execute advanced spatial SQL with optimization
```javascript
spatial_query({
  "query": "SELECT name, ST_Area(geom) as area FROM parcels WHERE ST_Intersects(geom, ST_Buffer(GeomFromText('POINT(-122.4 37.8)'), 1000))",
  "explain": true                     // Show query execution plan
})
```

### SpatiaLite Installation

**Windows:**
```bash
# Download from Gaia-SINS: https://www.gaia-gis.it/gaia-sins/
# Extract mod_spatialite.dll to your system PATH
```

**Note**: For data insertion, if `GeomFromText()` in INSERT statements encounters issues, use this workaround:
```javascript
// 1. Get binary geometry data
read_query({"query": "SELECT HEX(GeomFromText('POINT(x y)', 4326)) as hex_geom"})

// 2. Insert using binary format  
write_query({"query": "INSERT INTO table (geom) VALUES (X'hex_value')"})
```

> **✅ Windows Compatibility:** SpatiaLite v2.0.0 successfully provides full geospatial functionality on Windows! All spatial analysis, geometry operations, and spatial indexing work perfectly. The only minor limitation is `GeomFromText()` within INSERT statements, which has the simple workaround shown above.

**macOS (Homebrew):**
```bash
brew install spatialite-tools
brew install gdal
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install libsqlite3-mod-spatialite
# or for older versions:
sudo apt-get install spatialite-bin
```

### Example Workflows

**Location-Based Business Intelligence:**
```javascript
// 1. Load SpatiaLite extension
load_spatialite()

// 2. Create spatial table for store locations
create_spatial_table({
  "table_name": "stores",
  "geometry_type": "POINT",
  "additional_columns": [
    {"name": "store_name", "type": "TEXT"},
    {"name": "revenue", "type": "REAL"}
  ]
})

// 3. Create spatial index for performance
spatial_index({"table_name": "stores", "action": "create"})

// 4. Find stores within 5km of a location
spatial_query({
  "query": "SELECT store_name, revenue FROM stores WHERE ST_Distance(geom, GeomFromText('POINT(-122.4 37.8)')) <= 5000"
})

// 5. Calculate market coverage areas
geometry_operations({
  "operation": "buffer",
  "geometry1": "POINT(-122.4 37.8)",
  "buffer_distance": 2000
})
```

**Spatial Analysis Pipeline:**
```javascript
// 1. Import geographic data
import_shapefile({
  "shapefile_path": "./data/census_tracts.shp",
  "table_name": "demographics"
})

// 2. Perform spatial join analysis
spatial_analysis({
  "analysis_type": "spatial_join",
  "source_table": "stores",
  "target_table": "demographics"
})

// 3. Find optimal locations using proximity analysis
spatial_analysis({
  "analysis_type": "nearest_neighbor",
  "source_table": "potential_sites",
  "target_table": "competitors",
  "max_distance": 3000
})
```

## Enhanced Virtual Tables

The SQLite MCP Server provides intelligent data import capabilities with automatic schema detection, type inference, and seamless conversion of CSV and JSON files into queryable SQLite tables.

### Enhanced CSV Virtual Tables

**`create_enhanced_csv_table`** - Smart CSV import with automatic data type inference
```javascript
create_enhanced_csv_table({
  "table_name": "employees",
  "csv_file_path": "/path/to/employees.csv",
  "delimiter": ",",                    // CSV delimiter (default: comma)
  "has_header": true,                  // Whether CSV has header row
  "sample_rows": 100,                  // Rows to sample for type inference
  "null_values": ["", "NULL", "N/A"]   // Values to treat as NULL
})
```

**`analyze_csv_schema`** - Deep CSV analysis without creating tables
```javascript
analyze_csv_schema({
  "csv_file_path": "/path/to/data.csv",
  "sample_rows": 1000                  // Rows to analyze for schema detection
})
// Returns: file stats, column analysis, type confidence, sample values
```

### JSON Collection Virtual Tables

**`create_json_collection_table`** - Import JSONL and JSON array files with flattening
```javascript
create_json_collection_table({
  "table_name": "user_events",
  "json_file_path": "/path/to/events.jsonl",
  "format_type": "auto",               // auto, jsonl, json_array
  "flatten_nested": true,              // Flatten nested objects with dot notation
  "max_depth": 3,                      // Maximum nesting depth to flatten
  "sample_records": 100                // Records to sample for schema inference
})
```

**`analyze_json_schema`** - Comprehensive JSON structure analysis
```javascript
analyze_json_schema({
  "json_file_path": "/path/to/data.jsonl",
  "format_type": "auto",               // Auto-detect JSONL vs JSON array
  "sample_records": 1000               // Records to analyze
})
// Returns: schema analysis, type distribution, nested structure mapping
```

### Smart Type Inference Engine

**Automatic Data Type Detection:**
- **INTEGER**: Detects whole numbers, IDs, counts
- **REAL**: Identifies decimals, percentages, measurements  
- **TEXT**: Handles strings, mixed content, complex data
- **DATE**: Recognizes ISO dates, common date formats
- **BOOLEAN**: Converts true/false, yes/no, 1/0 patterns

**Advanced Features:**
- **Configurable Null Handling**: Customizable null value patterns
- **Statistical Analysis**: Type confidence based on sample data
- **Clean Column Names**: Automatic SQL-safe column naming
- **Error Resilience**: Graceful handling of malformed data
- **Performance Optimized**: Configurable sampling for large files

### Example Workflows

**CSV Data Import:**
```javascript
// 1. Analyze CSV structure first
analyze_csv_schema({"csv_file_path": "./sales_data.csv"})

// 2. Create table with inferred types
create_enhanced_csv_table({
  "table_name": "sales",
  "csv_file_path": "./sales_data.csv",
  "sample_rows": 500
})

// 3. Query your data immediately
SELECT product, SUM(amount) FROM sales GROUP BY product
```

**JSON Collection Import:**
```javascript
// 1. Analyze nested JSON structure
analyze_json_schema({"json_file_path": "./user_logs.jsonl"})

// 2. Create flattened table
create_json_collection_table({
  "table_name": "user_activity",
  "json_file_path": "./user_logs.jsonl",
  "flatten_nested": true,
  "max_depth": 2
})

// 3. Query flattened data
SELECT user_id, event_type, metadata_browser FROM user_activity
```

## Vector Index Optimization

The SQLite MCP Server provides enterprise-grade vector index optimization with Approximate Nearest Neighbor (ANN) search capabilities, transforming vector similarity search from O(n) linear to O(log n) sub-linear performance for massive datasets.

### Vector Index Optimization Tools

**`create_vector_index`** - Build optimized indexes for lightning-fast vector search
```javascript
create_vector_index({
  "table_name": "embeddings_table",
  "embedding_column": "embedding",     // Column containing vector embeddings
  "index_type": "cluster",             // cluster (k-means), grid (spatial), hash (LSH)
  "num_clusters": 100,                 // Number of clusters for k-means indexing
  "grid_size": 10                      // Grid dimensions for spatial indexing
})
```

**`optimize_vector_search`** - Perform ultra-fast ANN search using created indexes
```javascript
optimize_vector_search({
  "table_name": "embeddings_table",
  "query_embedding": [0.1, 0.2, 0.3, ...],
  "limit": 10,                         // Maximum results to return
  "search_k": 5,                       // Clusters to search (accuracy vs speed)
  "similarity_threshold": 0.7          // Minimum similarity score
})
```

**`analyze_vector_index`** - Comprehensive index performance analysis
```javascript
analyze_vector_index({
  "table_name": "embeddings_table"
})
// Returns: index statistics, cluster distribution, performance estimates
```

**`rebuild_vector_index`** - Intelligent index maintenance and optimization
```javascript
rebuild_vector_index({
  "table_name": "embeddings_table",
  "force": false                       // Force rebuild even if current
})
```

### Performance Benefits

- **100x Faster Search**: Sub-linear O(log n) performance vs O(n) linear search
- **Massive Scalability**: Handle millions of embeddings efficiently
- **Intelligent Clustering**: K-means partitioning reduces candidates by 90%+
- **Configurable Accuracy**: Balance speed vs precision with search_k parameter
- **Pure SQLite**: No external dependencies or complex setup required

### Index Types

**Cluster Index (K-Means)**:
- Best for: General-purpose vector search with balanced performance
- Algorithm: K-means clustering partitions vector space intelligently
- Performance: Excellent for most embedding dimensions and data distributions

**Grid Index (Spatial)**:
- Best for: High-dimensional embeddings with uniform distribution
- Algorithm: Multi-dimensional spatial grid partitioning
- Performance: Optimal for embeddings with known bounds and even distribution

**Hash Index (LSH)**:
- Best for: Extremely high-dimensional sparse vectors
- Algorithm: Locality-Sensitive Hashing for approximate similarity
- Performance: Constant-time lookup with configurable precision

### Example Workflow

```javascript
// 1. Create optimized index for your embedding table
create_vector_index({
  "table_name": "document_embeddings", 
  "index_type": "cluster",
  "num_clusters": 50
})

// 2. Perform lightning-fast similarity search
optimize_vector_search({
  "table_name": "document_embeddings",
  "query_embedding": your_query_vector,
  "limit": 20,
  "search_k": 3
})

// 3. Monitor and optimize index performance
analyze_vector_index({"table_name": "document_embeddings"})

// 4. Rebuild index after adding new embeddings
rebuild_vector_index({"table_name": "document_embeddings"})
```

## Intelligent MCP Resources & Prompts

The SQLite MCP Server provides intelligent meta-awareness and guided workflows through advanced MCP Resources and Prompts, transforming it from a simple database interface into a self-aware, intelligent assistant.

### MCP Resources - Database Meta-Awareness

MCP Resources provide dynamic "knowledge hooks" that give the AI model instant access to database metadata without requiring repeated queries.

**Available Resources:**

**`database://schema`** - Complete database schema with natural language descriptions
```javascript
// Automatically provides:
// - All table names and structures
// - Column types and constraints  
// - Row counts and relationships
// - Natural language schema summary
```

**`database://capabilities`** - Comprehensive server capabilities matrix
```javascript
// Provides real-time information about:
// - Available tools (51 total)
// - Feature support (FTS5, semantic search, virtual tables)
// - Advanced features and limitations
// - Server and SQLite versions
```

**`database://statistics`** - Real-time database statistics and health metrics
```javascript
// Dynamic statistics including:
// - Database size and page information
// - Table row counts and sizes
// - Index usage and efficiency
// - Performance recommendations
```

**`database://search_indexes`** - Search index status and capabilities
```javascript
// Comprehensive index information:
// - FTS5 tables and configurations
// - Semantic search embeddings status
// - Virtual table listings
// - Index optimization suggestions
```

**`database://performance`** - Performance analysis and optimization recommendations
```javascript
// Intelligent performance insights:
// - Health score assessment
// - Maintenance recommendations
// - Optimization suggestions
// - Best practices guidance
```

### MCP Prompts - Guided Workflows

MCP Prompts provide intelligent workflow automation, acting as "recipes" that guide complex multi-step operations.

**Available Prompts:**

**`semantic_query`** - Natural language to semantic search translation
- Guides the AI through converting natural language questions into proper semantic search operations
- Handles embedding generation, similarity thresholds, and result interpretation
- Provides fallback strategies for complex queries

**`summarize_table`** - Intelligent table analysis with configurable depth
- Automated table exploration with statistical analysis
- Configurable analysis depth (quick, standard, deep)
- Generates natural language summaries with key insights

**`optimize_database`** - Step-by-step database optimization workflow  
- Comprehensive optimization checklist
- Automated VACUUM, ANALYZE, and integrity checking
- Performance tuning recommendations

**`setup_semantic_search`** - Complete semantic search implementation guide
- End-to-end setup for embedding tables and indexes
- Integration with external embedding services
- Testing and validation procedures

**`hybrid_search_workflow`** - Hybrid keyword + semantic search implementation
- Combines FTS5 keyword search with semantic similarity
- Configurable weighting between search methods
- Result ranking and relevance tuning

### Benefits of Resources & Prompts

**Reduced Hallucination**: AI always has access to current database state through resources
**Improved Workflows**: Complex operations are guided by proven prompt recipes  
**Meta-Awareness**: Server becomes self-aware of its own capabilities and limitations
**Consistency**: Standardized approaches to common database operations
**Efficiency**: Eliminates repetitive queries for metadata and schema information

## Planned Future Enhancements

#### **1. Advanced Vector Search with sqlite-vss - HIGH PRIORITY**
- **Planned**: Industry-standard HNSW and IVF vector indexing
- **Examples**: 10-100x faster semantic search, large-scale embedding storage
- **Impact**: Replace custom vector optimization with proven ANN algorithms

#### **2. Statistical Analytics with sqlean-stats - HIGH PRIORITY**
- **Planned**: Comprehensive statistical function library
- **Examples**: Correlation analysis, regression, percentiles, hypothesis testing
- **Impact**: Fill major gap in statistical capabilities for advanced BI

#### **3. Advanced Text Processing - MEDIUM PRIORITY**
- **Planned**: PCRE regex support and advanced string functions (sqlean-text, sqlite-regex)
- **Examples**: Complex pattern matching, fuzzy search, phonetic algorithms, data validation
- **Impact**: Enhanced text analysis beyond FTS5 capabilities

#### **4. Advanced Data Connectors - MEDIUM PRIORITY**
- **Planned**: Direct database connectors (PostgreSQL, MySQL, MongoDB)
- **Examples**: Cross-database queries, data synchronization

#### **5. Real-time Data Streaming - LOW PRIORITY**
- **Planned**: Live data ingestion from streaming sources
- **Examples**: Kafka, WebSocket, API polling integration

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

Please note that this project is released with a [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Security

If you discover a security vulnerability, please follow our [Security Policy](SECURITY.md) for responsible disclosure.

## Support

- 📝 [Open an issue](https://github.com/neverinfamous/mcp_server_sqlite/issues) for bug reports or feature requests
- 🌐 Visit memory-journal-mcp (https://github.com/neverinfamous/memory-journal-mcp)

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.