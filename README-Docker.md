# SQLite MCP Server - Docker Quick Start

*Lightweight, containerized SQLite database server with AI-native features*

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

- **40 Tools**: Complete SQLite operations + advanced vector optimization
- **7 Intelligent Resources**: Real-time database meta-awareness
- **7 Guided Prompts**: Workflow automation for complex operations
- **Vector Index Optimization**: ANN search with k-means clustering for 100x performance
- **AI-Native**: Semantic search, vector storage, hybrid search
- **Enterprise Ready**: Backup/restore, integrity checks, optimization

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
