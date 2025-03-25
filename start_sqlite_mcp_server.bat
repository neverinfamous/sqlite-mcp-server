@echo off
cd /d %~dp0
echo Starting SQLite MCP Server...
venv\Scripts\python start_mcp_sqlite.py --db-path "C:\Users\chris\Desktop\adamic\mcp\test.db"
