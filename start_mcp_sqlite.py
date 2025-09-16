#!/usr/bin/env python
import asyncio
import argparse
import logging
import os
from mcp_server_sqlite.server import main

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'sqlite_mcp.log'))
    ]
)

logger = logging.getLogger('mcp_sqlite_runner')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Start SQLite MCP Server')
    parser.add_argument('--db-path', type=str, default='./data.db', help='Path to the SQLite database file (default: ./data.db in current directory)')
    args = parser.parse_args()
    
    logger.info(f"Starting SQLite MCP Server with database path: {args.db_path}")
    asyncio.run(main(args.db_path))
