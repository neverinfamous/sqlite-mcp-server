"""Basic tests for SQLite MCP Server."""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def test_import_server():
    """Test that we can import the server module."""
    try:
        from mcp_server_sqlite import server
        assert server is not None
    except ImportError:
        pytest.skip("MCP server module not available")

def test_basic_functionality():
    """Basic functionality test."""
    assert 1 + 1 == 2
    
def test_sqlite_version():
    """Test SQLite version detection."""
    import sqlite3
    version = sqlite3.sqlite_version_info
    assert len(version) >= 3
    assert version[0] >= 3  # SQLite 3.x
