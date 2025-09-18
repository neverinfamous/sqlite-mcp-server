# SQLite MCP Server

*Last Updated September 17, 2025 7:35 AM EST - v2.2.0*

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

**Claude Desktop (mcp.json)**:
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

- **Advanced Text Processing**: Comprehensive text analysis toolkit with 8 specialized tools: PCRE regex extraction/replacement, fuzzy matching with Levenshtein distance, phonetic matching (Soundex/Metaphone), text similarity analysis (Cosine/Jaccard), normalization operations, pattern validation, advanced multi-method search, and comprehensive text validation
- **Statistical Analysis Library**: Comprehensive statistical functions for data analysis including descriptive statistics, percentile analysis, and time series analysis
- **JSONB Binary Storage**: Efficient binary JSON storage for improved performance and reduced storage requirements
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
- **SpatiaLite Geospatial Analytics**: Enterprise-grade GIS capabilities with spatial indexing and geometric operations
- **Enhanced Virtual Tables**: Smart CSV/JSON import with automatic data type inference and schema analysis (67 tools total)
- **Full-Text Search (FTS5)**: Comprehensive FTS5 implementation with table creation, index management, and enhanced search with BM25 ranking and snippets
- **Backup/Restore Operations**: Enterprise-grade backup and restore capabilities with SQLite backup API, integrity verification, and safety confirmations
- **Advanced PRAGMA Operations**: Comprehensive SQLite configuration management, performance optimization, and database introspection tools
- **Virtual Table Management**: Complete virtual table lifecycle management for R-Tree spatial indexing, CSV file access, and sequence generation
- **Semantic/Vector Search**: AI-native semantic search with embedding storage, cosine similarity, and hybrid keyword+semantic ranking
- **Vector Index Optimization**: Approximate Nearest Neighbor (ANN) search with k-means clustering and spatial indexing for sub-linear O(log n) performance
- **Intelligent MCP Resources**: Dynamic database meta-awareness with real-time schema, capabilities, statistics, search indexes, and performance insights
- **Guided MCP Prompts**: Intelligent workflow automation with semantic query translation, table summarization, database optimization, and hybrid search recipes
- **Advanced SQLite Engine**: Upgraded to SQLite 3.50.4 with significant performance enhancements
- **WAL Mode Compatible**: Works alongside the existing Write-Ahead Logging (WAL) journal mode
<br><br>

⚠️ Tool Count Consideration<br><br>
The SQLite MCP Server exposes 67 tools by default. MCP clients such as Cursor typically start warning users around 80 tools total, and stability issues can appear above ~100–120 tools depending on your setup. To keep your workspace responsive, you can disable any tools you don’t need directly in your MCP client settings. This makes it easy to slim down the server for your specific use case (e.g., only enabling query, JSON, or vector tools).

## Database Configuration

- **Auto-creates** `sqlite_mcp.db` in your project root if none exists because **MCP operations require persistent storage** between tool calls
- **Connects to existing databases** - works with any SQLite file you specify

The server automatically detects project structure and creates appropriate database locations, supporting both relative and absolute paths for maximum flexibility.

### Statistical Analysis Workflow

1. **Explore Data Distribution**: Use `descriptive_statistics` to understand central tendency and variability
2. **Identify Quartiles**: Apply `percentile_analysis` to find data distribution boundaries  
3. **Analyze Trends**: Employ `moving_averages` for time series pattern recognition
4. **Generate Insights**: Combine statistical results with business context using `append_insight`

### Example Analysis Session

```javascript
// 1. Get overview of sales performance
descriptive_statistics({
  table_name: "monthly_sales",
  column_name: "revenue"
})

// 2. Understand distribution 
percentile_analysis({
  table_name: "monthly_sales", 
  column_name: "revenue",
  percentiles: [10, 25, 50, 75, 90]
})

// 3. Analyze trends over time
moving_averages({
  table_name: "monthly_sales",
  value_column: "revenue",
  time_column: "month", 
  window_sizes: [3, 6, 12]
})
```

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
- `v2.2.0` - Specific version

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

## Docker Hub Authentication (For Contributors)

If you need to push updates to the Docker Hub repository, authenticate using a Personal Access Token:

```bash
# Interactive login (recommended)
docker login -u writenotenow
# Enter your Docker Hub Personal Access Token when prompted

# Command line login
echo "YOUR_DOCKER_HUB_PAT_TOKEN" | docker login -u writenotenow --password-stdin
```

**Authentication Notes:**
- Use Docker Hub Personal Access Token, not password
- Create PAT at: https://hub.docker.com/settings/security
- Required permissions: Read, Write, Delete

## Links

- **GitHub**: https://github.com/neverinfamous/sqlite-mcp-server
- **Docker Hub**: https://hub.docker.com/r/writenotenow/sqlite-mcp-server
- **Full Documentation**: See main README.md for complete feature documentation