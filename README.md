# SQLite MCP Server

*Last Updated September 17, 2025 7:34 AM EST - v2.2.0*

## Overview

The SQLite MCP Server offers advanced database and business intelligence capabilities built on an upgraded SQLite 3.50.4 engine. It provides a comprehensive suite of tools for advanced text processing, statistical analysis, and SpatiaLite geospatial analytics, all within a robust, transaction-safe framework.

## Key Features

- **Advanced Text Processing**: Comprehensive text analysis toolkit with 8 specialized tools: PCRE regex extraction/replacement, fuzzy matching with Levenshtein distance, phonetic matching (Soundex/Metaphone), text similarity analysis (Cosine/Jaccard), normalization operations, pattern validation, advanced multi-method search, and comprehensive text validation
- **Statistical Analysis Library**: Comprehensive statistical functions for data analysis including descriptive statistics, percentile analysis, and time series analysis
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

---

## Tool Reference

The server exposes dynamic resources and a full suite of tools for various workflows.

### Query and Schema Tools

These tools manage database structure and content.

- **`read_query`**: Execute `SELECT` queries with support for window functions and parameter binding.
- **`write_query`**: Execute `INSERT`, `UPDATE`, or `DELETE` queries with transaction safety.
- **`create_table`**: Create new tables in the database.
- **`list_tables`**: Get a list of all tables.
- **`describe_table`**: Show schema information for a specific table.

### Advanced Toolkits

- **Advanced Text Processing**: Use functions like `regex_extract`, `fuzzy_match`, and `text_similarity` for in-depth text analysis.
- **Statistical Analysis**: Access functions like `descriptive_statistics`, `percentile_analysis`, and `moving_averages` for data analysis.
- **FTS5 Management**: Use `create_fts_table`, `fts_search`, and `rebuild_fts_index` to manage and use full-text search.
- **Backup & Restore**: Use `backup_database` and `restore_database` for enterprise-grade database maintenance.
- **Advanced PRAGMA Operations**: Manage database settings with `pragma_settings`, optimize performance with `pragma_optimize`, and get detailed introspection with `pragma_table_info`.

For a complete list of tools and their JSON request formats, refer to the source documentation.

---

## Core Enhancements

### 1. JSONB Binary Storage

The server leverages SQLite 3.45's JSONB binary storage format, providing:
- **Reduced Storage Size**: Up to 15% space savings.
- **Faster Parsing**: Eliminates the need to re-parse JSON text for each operation.
- **Type Preservation**: Maintains data types without text conversion.
- **Usage**: JSON strings are automatically stored efficiently. For optimal handling, use parameter binding.

### 2. Transaction Safety

All write operations (`INSERT`, `UPDATE`, `DELETE`) are automatically wrapped in transactions. If an operation fails, all changes are automatically rolled back, preventing partial writes and reducing the risk of database corruption.

### 3. Foreign Key Constraint Enforcement

Foreign keys are now automatically enabled and enforced for every database connection. This ensures consistent data integrity and prevents orphaned records.

---

## Best Practices

### Standard Query Workflow
1. Use `list_tables` and `describe_table` to verify schemas.
2. Construct queries using exact column names.
3. For dynamic queries, always use parameter binding to prevent SQL injection.
4. For JSON operations, use standard JSON strings; the server automatically handles the rest.

### SQLite-Specific Considerations
- Use `INTEGER PRIMARY KEY` instead of `AUTO_INCREMENT`.
- Use `TEXT` for strings instead of `VARCHAR`.
- For `JSON` data, use standard strings; the server handles the underlying JSONB storage.

---

## Installation & Deployment

### Core Requirements
- Python 3.10+
- SQLite 3.45.0+
- MCP 1.14.0+

### Deployment Options

- **Smithery (Recommended)**: A one-click deployment for instant, auto-scaling, and globally distributed hosting.
- **Local Installation**: Clone the repository, install dependencies with `pip install -r requirements.txt`, and run `python start_sqlite_mcp.py`.
- **Docker Deployment**: Use the provided `Dockerfile` to build and run a containerized version.

### Database Configuration
The server features a **zero-configuration start** and will automatically create a persistent database file at `sqlite_mcp.db` if one isn't specified. You can also connect to an existing database using the `--db-path` argument.

---

## Troubleshooting

- **JSON Errors**: Use the `validate_json` tool to check for malformed JSON.
- **Database Locked**: This can occur during concurrent transactions; check for other long-running operations.
- **Foreign Key Failure**: Verify that the referenced record exists before attempting to insert or update.
- **Performance**: Consider running `VACUUM` on the database to improve performance.

---

## Attribution

This project is based on the original SQLite MCP Server from the [Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers/tree/2025.4.24/src/sqlite) repository. Our sincere gratitude goes to the original developers and the Model Context Protocol team for their foundational work.

**Original Authors**: Model Context Protocol Team  
**Original Repository**: [https://github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)  
**License**: MIT License