"""SQLite version checking utilities"""
import sqlite3

def check_sqlite_version():
    """Check SQLite version and capabilities"""
    version = sqlite3.sqlite_version
    version_info = sqlite3.sqlite_version_info
    
    # Check for JSONB support (available in SQLite 3.45.0+)
    has_jsonb_support = version_info >= (3, 45, 0)
    
    return {
        'version': version,
        'version_info': version_info,
        'has_jsonb_support': has_jsonb_support
    }