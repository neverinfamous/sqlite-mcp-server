# SQLite MCP Server

*Last Updated: September 18, 2025 5:11 PM EST – v2.2.0*

The SQLite MCP Server transforms SQLite into a powerful, AI-ready database engine. It combines standard relational operations with advanced analytics, text and vector search, geospatial capabilities, and intelligent workflow automation. By layering business intelligence tools, semantic resources, and guided prompts on top of SQLite, it enables both developers and AI assistants to interact with data more naturally and effectively.

## 🚀 Quick Try

Copy and paste to run with Docker instantly:

```bash
docker run -i --rm \
  -v $(pwd):/workspace \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/sqlite_mcp.db
```

## Quick Start

### Pull and Run

```bash
# Pull from Docker Hub (recommended)
docker pull writenotenow/sqlite-mcp-server:latest

# Or pull specific version
docker pull writenotenow/sqlite-mcp-server:v2.2.0

# Run with volume mount
docker run -i --rm \
  -v /path/to/your/data:/workspace \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/database.db
```

### MCP Client Configuration

**Claude Desktop (mcp.json):**

```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/path/to/your/project:/workspace",
        "writenotenow/sqlite-mcp-server:latest",
        "--db-path", "/workspace/database.db"
      ]
    }
  }
}
```

**Cursor IDE:**

```json
{
  "sqlite-mcp-server": {
    "command": "docker",
    "args": [
      "run", "-i", "--rm", 
      "-v", "${workspaceFolder}:/workspace",
      "writenotenow/sqlite-mcp-server:latest",
      "--db-path", "/workspace/database.db"
    ]
  }
}
```

## ✅ Quick Test - Verify Everything Works

**Test all 67 tools in 30 seconds:**

```bash
# Quick smoke test
python test_runner.py --quick

# Standard comprehensive test (recommended)
python test_runner.py --standard

# Full test suite with edge cases
python test_runner.py --full
```

**Expected output:**
```
🚀 SQLite MCP Server Comprehensive Test Suite v2.2.0
================================================================

🔍 Environment Detection:
  ✅ SQLite 3.50.2 (JSONB supported)
  ✅ Python 3.12.11  
  ✅ MCP 1.14.0

📊 Testing 67 Tools across 13 categories...

✅ Core Database Operations (8/8 passed)
✅ JSON Operations (12/12 passed)  
✅ Text Processing (8/8 passed)
🎉 SUCCESS: 63/67 tools tested successfully!
```

## Key Features

* **Advanced Text Processing**: Comprehensive text analysis toolkit with 8 specialized tools: PCRE regex extraction/replacement, fuzzy matching with Levenshtein distance, phonetic matching (Soundex/Metaphone), text similarity analysis (Cosine/Jaccard), normalization operations, pattern validation, advanced multi-method search, and comprehensive text validation
* **Statistical Analysis Library**: Comprehensive statistical functions for data analysis including descriptive statistics, percentile analysis, and time series analysis
* **JSONB Binary Storage**: Efficient binary JSON storage for improved performance and reduced storage requirements
* **Transaction Safety**: All write operations automatically wrapped in transactions with proper rollback on errors
* **Foreign Key Enforcement**: Automatic enforcement of foreign key constraints across all connections
* **Advanced SQL Support**: Complex queries including window functions, subqueries, and advanced filtering
* **Business Intelligence**: Integrated memo resource for capturing business insights during analysis
* **Enhanced Error Handling**: Detailed diagnostics for JSON-related errors with specific suggestions for fixing issues
* **Multi-Level Caching**: Hierarchical caching for optimal performance
* **Pattern Recognition**: Automatic optimization of frequently executed queries
* **JSON Validation**: Prevents invalid JSON from being stored in the database
* **WAL Mode Compatible**: Works alongside the existing Write-Ahead Logging (WAL) journal mode
* **Comprehensive Schema Tools**: Enhanced tools for exploring and documenting database structure
* **Database Administration Tools**: Complete suite of maintenance tools including VACUUM, ANALYZE, integrity checks, performance statistics, and index usage analysis
* **Full-Text Search (FTS5)**: Comprehensive FTS5 implementation with table creation, index management, and enhanced search with BM25 ranking and snippets
* **Backup/Restore Operations**: Enterprise-grade backup and restore capabilities with SQLite backup API, integrity verification, and safety confirmations
* **Advanced PRAGMA Operations**: Comprehensive SQLite configuration management, performance optimization, and database introspection tools
* **Virtual Table Management**: Complete virtual table lifecycle management for R-Tree spatial indexing, CSV file access, and sequence generation
* **SpatiaLite Geospatial Analytics**: Enterprise-grade GIS capabilities with spatial indexing, geometric operations, and comprehensive spatial analysis
* **Enhanced Virtual Tables**: Smart CSV/JSON import with automatic data type inference, nested object flattening, and schema analysis
* **Semantic/Vector Search**: AI-native semantic search with embedding storage, cosine similarity, and hybrid keyword+semantic ranking
* **Vector Index Optimization**: Approximate Nearest Neighbor (ANN) search with k-means clustering and spatial indexing for sub-linear O(log n) performance
* **Intelligent MCP Resources**: Dynamic database meta-awareness with real-time schema, capabilities, statistics, search indexes, and performance insights
* **Guided MCP Prompts**: Intelligent workflow automation with semantic query translation, table summarization, database optimization, and hybrid search recipes

⚠️ **Tool Count Consideration**
The SQLite MCP Server exposes 67 tools by default. MCP clients like Cursor may warn around 80 tools and can become unstable past \~100–120. Disable unneeded tools in client settings to slim down usage.

## Database Configuration

* **Auto-creates** `sqlite_mcp.db` in your project root if none exists (MCP requires persistence).
* **Connects to existing databases** via any SQLite file path.
* **Supports both relative and absolute paths**.

## Statistical Analysis Workflow

1. Explore data distribution → `descriptive_statistics`
2. Identify quartiles → `percentile_analysis`
3. Analyze trends → `moving_averages`
4. Generate insights → `append_insight`

```javascript
descriptive_statistics({ table_name: "monthly_sales", column_name: "revenue" })
percentile_analysis({ table_name: "monthly_sales", column_name: "revenue", percentiles: [10,25,50,75,90] })
moving_averages({ table_name: "monthly_sales", value_column: "revenue", time_column: "month", window_sizes: [3,6,12] })
```

---

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

---

## Available Tags

* `latest` – latest stable release
* `v2.2.0` – pinned version

---

## Examples

**Data Analysis Project**

```bash
docker run -i --rm \
  -v /Users/analyst/project:/workspace \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/analysis.db
```

**Development Environment**

```bash
docker run -i --rm \
  -v $(pwd):/workspace \
  -e SQLITE_DEBUG=true \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/dev.db
```

**CI/CD Testing**

```bash
docker run -i --rm \
  -v /tmp/test-data:/workspace \
  writenotenow/sqlite-mcp-server:latest \
  --db-path :memory:
```

---

## Advanced Usage

**Multi-Architecture Support**

* `linux/amd64` – Intel/AMD 64-bit
* `linux/arm64` – Apple Silicon, ARM64

**Resource Limits**

```bash
docker run -i --rm \
  --memory=512m --cpus=1.0 \
  -v $(pwd):/workspace \
  writenotenow/sqlite-mcp-server:latest
```

**Persistent Volumes**

```bash
docker volume create sqlite-data

docker run -i --rm \
  -v sqlite-data:/data \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /data/persistent.db
```

---

## Troubleshooting

* **Permission Issues**: Ensure volume mount paths have proper permissions
* **Database Not Found**: Check volume mount and file paths
* **Connection Issues**: Verify MCP client configuration

---

## Links

* **GitHub**: [https://github.com/neverinfamous/sqlite-mcp-server](https://github.com/neverinfamous/sqlite-mcp-server)
* **Full Documentation**: See main README.md for complete feature documentation