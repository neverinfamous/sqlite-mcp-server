# SQLite MCP Server

*Last Updated September 17, 2025 1:10 AM EST - v1.9.3*

*Lightweight, containerized SQLite database server with AI-native features*

## 🚀 Zero-Configuration Database
**No database setup required!** The server automatically creates and manages persistent SQLite databases **because MCP operations need persistent storage**:
- **Auto-creates** `sqlite_mcp.db` files as needed (MCP tools require shared data storage)
- **Why create a file?** Tables, indexes, and data must persist between MCP tool calls
- **Persists all data** between container runs
- **Connects to any existing** SQLite database
- **Works immediately** - mount your data directory and go!

## Quick Start

### Pull and Run
```bash
# Pull latest image
docker pull ghcr.io/neverinfamous/sqlite-mcp-server:latest

# Run with volume mount
docker run -i --rm \
  -v /path/to/your/data:/workspace \
  ghcr.io/neverinfamous/sqlite-mcp-server:latest \
  --db-path /workspace/database.db
```

### MCP Client Configuration

**Claude Desktop (mcp.json)**:
```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/path/to/your/project:/workspace",
        "ghcr.io/neverinfamous/sqlite-mcp-server:latest",
        "--db-path", "/workspace/database.db"
      ]
    }
  }
}
```

**Cursor IDE**:
```json
{
  "sqlite-mcp-server": {
    "command": "docker",
    "args": [
      "run", "-i", "--rm", 
      "-v", "${workspaceFolder}:/workspace",
      "ghcr.io/neverinfamous/sqlite-mcp-server:latest",
      "--db-path", "/workspace/database.db"
    ]
  }
}
```

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
- **Enhanced Virtual Tables**: Smart CSV/JSON import with automatic data type inference and schema analysis (44 tools total)
- **Full-Text Search (FTS5)**: Comprehensive FTS5 implementation with table creation, index management, and enhanced search with BM25 ranking and snippets
- **Backup/Restore Operations**: Enterprise-grade backup and restore capabilities with SQLite backup API, integrity verification, and safety confirmations
- **Advanced PRAGMA Operations**: Comprehensive SQLite configuration management, performance optimization, and database introspection tools
- **Virtual Table Management**: Complete virtual table lifecycle management for R-Tree spatial indexing, CSV file access, and sequence generation
- **Semantic/Vector Search**: AI-native semantic search with embedding storage, cosine similarity, and hybrid keyword+semantic ranking
- **Vector Index Optimization**: Approximate Nearest Neighbor (ANN) search with k-means clustering and spatial indexing for sub-linear O(log n) performance
- **Intelligent MCP Resources**: Dynamic database meta-awareness with real-time schema, capabilities, statistics, search indexes, and performance insights
- **Guided MCP Prompts**: Intelligent workflow automation with semantic query translation, table summarization, database optimization, and hybrid search recipes
- **Advanced SQLite Engine**: Upgraded to SQLite 3.50.4 with significant performance enhancements

## Container Options

### Database Locations
```bash
# Project database
-v /host/project:/workspace --db-path /workspace/data/database.db

# Dedicated data volume  
-v sqlite-data:/data --db-path /data/database.db

# Temporary database
--db-path :memory:
```

### Environment Variables
```bash
# Debug mode
-e SQLITE_DEBUG=true

# Custom log directory
-e SQLITE_LOG_DIR=/workspace/logs
```

## Available Tags

- `latest` - Latest stable release
- `v1.8.0` - Specific version
- `main` - Development build

## Examples

### Data Analysis Project
```bash
docker run -i --rm \
  -v /Users/analyst/project:/workspace \
  ghcr.io/neverinfamous/sqlite-mcp-server:latest \
  --db-path /workspace/analysis.db
```

### Development Environment
```bash
docker run -i --rm \
  -v $(pwd):/workspace \
  -e SQLITE_DEBUG=true \
  ghcr.io/neverinfamous/sqlite-mcp-server:latest \
  --db-path /workspace/dev.db
```

### CI/CD Testing
```bash
docker run -i --rm \
  -v /tmp/test-data:/workspace \
  ghcr.io/neverinfamous/sqlite-mcp-server:latest \
  --db-path :memory:
```

## Advanced Usage

### Multi-Architecture Support
- `linux/amd64` - Intel/AMD 64-bit
- `linux/arm64` - Apple Silicon, ARM64

### Resource Limits
```bash
docker run -i --rm \
  --memory=512m --cpus=1.0 \
  -v $(pwd):/workspace \
  ghcr.io/neverinfamous/sqlite-mcp-server:latest
```

### Persistent Volumes
```bash
# Create named volume
docker volume create sqlite-data

# Use named volume
docker run -i --rm \
  -v sqlite-data:/data \
  ghcr.io/neverinfamous/sqlite-mcp-server:latest \
  --db-path /data/persistent.db
```

## Troubleshooting

**Permission Issues**: Ensure volume mount paths have proper permissions
**Database Not Found**: Check volume mount and file paths
**Connection Issues**: Verify MCP client configuration

## Links

- **GitHub**: https://github.com/neverinfamous/sqlite-mcp-server
- **Docker Hub**: https://hub.docker.com/r/neverinfamous/sqlite-mcp-server
- **Full Documentation**: See main README.md for complete feature documentation

---

*SQLite MCP Server v1.9.0 - Transform your database into an intelligent, self-aware assistant with enterprise-grade vector optimization*
