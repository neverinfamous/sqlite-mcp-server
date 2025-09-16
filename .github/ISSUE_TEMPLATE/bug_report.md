---
name: Bug report
about: Create a report to help us improve the SQLite MCP Server
title: '[BUG] '
labels: 'bug'
assignees: 'neverinfamous'

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Set up MCP server with '...'
2. Execute query '....'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Error output**
If applicable, add the full error output/traceback to help explain your problem.

```
Paste error output here
```

**Environment (please complete the following information):**
 - OS: [e.g. macOS, Windows, Linux]
 - Python version: [e.g. 3.12]
 - SQLite version: [run `python -c "import sqlite3; print(sqlite3.sqlite_version)"`]
 - MCP Server version: [e.g. 1.0.0]
 - Installation method: [e.g. pip, Docker, source]

**Database information:**
 - Database size: [e.g. 100MB, 1GB]
 - Number of tables: [approximate]
 - Using JSONB features: [yes/no]
 - Transaction safety enabled: [yes/no]

**Additional context**
Add any other context about the problem here.

**Configuration**
If relevant, share your MCP server configuration (remove sensitive data):

```json
{
  "mcpServers": {
    "sqlite-server": {
      "command": "...",
      "args": ["..."]
    }
  }
}
```