# Lite MCP Server with JSONB Support

*Last Updated: March 25, 2025*

## Overview

The Lite MCP Server (formerly known as SQLite MCP Server) is a Model Context Protocol (MCP) server implementation that provides advanced database interaction capabilities through SQLite with JSONB support. This server includes enhanced JSON handling with binary storage format for improved efficiency, detailed error diagnostics, and validation features.

## Key Features

- **JSONB Binary Storage**: Efficient JSON storage with ~15% space savings
- **Advanced SQL Support**: Complex queries including window functions and advanced filtering
- **Hyperdrive Acceleration**: Ultra-fast query processing with 2-9ms response times
- **Business Intelligence**: Integrated memo resource for capturing insights during analysis
- **Enhanced Error Handling**: Detailed diagnostics for JSON operations
- **JSON Validation**: Prevents invalid JSON from being stored in the database
- **Comprehensive Schema Tools**: Tools for exploring and documenting database structure

## Installation Requirements

- **SQLite 3.45.0+**: Core database engine with JSONB support
- **Node.js**: Runtime environment
- **Visual Studio with C++ Build Tools**: Required for native module compilation
- **better-sqlite3**: High-performance SQLite3 database library for Node.js

## Usage

### Query Tools

- **`read_query`**: Execute SELECT queries
  ```javascript
  read_query({
    "query": "SELECT * FROM table_name WHERE id = ?"
    "params": [123]
  })
  ```

- **`write_query`**: Execute INSERT, UPDATE, or DELETE queries
  ```javascript
  write_query({
    "query": "INSERT INTO table_name (column1, column2) VALUES (?, ?)",
    "params": ["value1", "value2"]
  })
  ```

- **`create_table`**: Create new tables in the database
  ```javascript
  create_table({
    "query": "CREATE TABLE table_name (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)"
  })
  ```

### Schema Tools

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

### JSONB Usage

For optimal JSON handling, always use JSONB format:

```javascript
// Insert JSON data with JSONB
write_query({
  "query": "INSERT INTO table_name (json_column) VALUES (jsonb(?))",
  "params": [JSON.stringify({"key": "value"})]
})

// Update JSON data with JSONB
write_query({
  "query": "UPDATE table_name SET json_column = jsonb(?) WHERE id = ?",
  "params": [JSON.stringify({"key": "updated_value"}), 123]
})

// Query JSON data with standard JSON functions
read_query({
  "query": "SELECT json_extract(json_column, '$.key') FROM table_name WHERE id = ?",
  "params": [123]
})
```

## License

MIT
