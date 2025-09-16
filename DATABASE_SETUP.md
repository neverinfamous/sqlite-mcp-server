# SQLite MCP Server - Database Setup Guide

## Flexible Database Configuration

The SQLite MCP Server supports flexible database configuration to work with any SQLite database file in any location.

### Quick Start

**Automatic Setup (Recommended)**:
```bash
python start_sqlite_mcp.py --create-data-dir
```
This creates a `data/` directory in your project root and places the database there.

**Use Existing Database**:
```bash
python start_sqlite_mcp.py --db-path /path/to/your/database.db
```

### Configuration Options

#### 1. Auto-Detection (Default)
The server automatically detects your project structure:

```bash
python start_sqlite_mcp.py
```

**Detection Logic**:
1. Looks for project root indicators (`.git`, `pyproject.toml`, `package.json`, etc.)
2. Checks for existing `data/` subdirectory
3. Places database in project root if no `data/` directory exists
4. Falls back to current directory

#### 2. Explicit Database Path
```bash
python start_sqlite_mcp.py --db-path ./my-database.db
python start_sqlite_mcp.py --db-path /absolute/path/to/database.db
python start_sqlite_mcp.py --db-path :memory:  # In-memory database
```

#### 3. Project Root Override
```bash
python start_sqlite_mcp.py --project-root /path/to/project --db-name myapp.db
```

#### 4. Create Data Directory
```bash
python start_sqlite_mcp.py --create-data-dir --db-name myapp.db
```
This creates `data/myapp.db` in your project root.

### MCP Client Configuration

#### For Claude Desktop (mcp.json)
```json
{
  "mcpServers": {
    "sqlite-local": {
      "command": "python",
      "args": [
        "/path/to/sqlite-mcp-server/start_sqlite_mcp.py",
        "--db-path",
        "/path/to/your/database.db"
      ]
    }
  }
}
```

#### For Docker Deployment
```json
{
  "mcpServers": {
    "sqlite-docker": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/host/project/path:/workspace",
        "sqlite-mcp-server",
        "--db-path", "/workspace/data/database.db"
      ]
    }
  }
}
```

### Database Location Best Practices

#### ✅ Recommended Locations
- **`./data/database.db`** - Project data directory (best for version control)
- **`./database.db`** - Project root (simple, good for small projects)
- **`~/.local/share/myapp/database.db`** - User data directory (cross-platform)

#### ⚠️ Consider Carefully
- **Absolute paths** - Less portable between environments
- **System directories** - May have permission issues
- **Temporary directories** - Data may be lost

#### ❌ Avoid
- **`:memory:`** - Data lost when server stops (good for testing only)
- **Read-only locations** - Server needs write access
- **Network paths** - May have performance/reliability issues

### Examples

#### Personal Project
```bash
cd ~/my-project
python /path/to/sqlite-mcp-server/start_sqlite_mcp.py --create-data-dir
# Creates ~/my-project/data/database.db
```

#### Team Project with Existing Database
```bash
cd /team/project
python /path/to/sqlite-mcp-server/start_sqlite_mcp.py --db-path ./shared-data/team.db
# Uses /team/project/shared-data/team.db
```

#### Development vs Production
```bash
# Development
python start_sqlite_mcp.py --db-path ./dev-database.db

# Production  
python start_sqlite_mcp.py --db-path /var/lib/myapp/production.db
```

### Troubleshooting

**Database Not Found**:
- Check file path and permissions
- Ensure parent directories exist
- Verify the server has write access

**Permission Denied**:
- Use a location where you have write permissions
- Consider using `--create-data-dir` for automatic setup

**Path Issues on Windows**:
- Use forward slashes or double backslashes in paths
- Consider using relative paths for portability

### Security Considerations

- **File Permissions**: Ensure database file has appropriate read/write permissions
- **Location Security**: Don't place databases in web-accessible directories  
- **Backup Strategy**: Regular backups for important data
- **Access Control**: Consider file system permissions for multi-user environments