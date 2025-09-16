@echo off
cd /d %~dp0
echo Starting SQLite MCP Server with flexible database path detection...
python start_sqlite_mcp.py --create-data-dir
