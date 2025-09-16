"""
Script to enable transaction safety for the SQLite MCP Server

This script modifies the server.py file to import and use our transaction safety module.
"""

import sys
import os
import re
from pathlib import Path

def enable_transaction_safety():
    """
    Enable transaction safety by updating the server.py file
    """
    # Path to the server.py file
    server_path = Path(__file__).parent / "server.py"
    
    # Check if the file exists
    if not server_path.exists():
        print(f"Error: server.py not found at {server_path}")
        return False
    
    # Read the server.py file
    with open(server_path, "r") as f:
        content = f.read()
    
    # Check if transaction safety is already enabled
    if "transaction_safety" in content or "db_integration" in content:
        print("Transaction safety already enabled")
        return True
    
    # Add import for db_integration
    import_pattern = re.compile(r"from \.jsonb_utils import .*?\n")
    import_match = import_pattern.search(content)
    
    if import_match:
        # Add our import after the jsonb_utils import
        new_import = import_match.group(0) + "from .db_integration import DatabaseIntegration\n"
        content = content[:import_match.start()] + new_import + content[import_match.end():]
    else:
        print("Error: Could not find jsonb_utils import pattern")
        return False
    
    # Find the _init_database method
    init_pattern = re.compile(r"def _init_database\(self\):.*?conn\.close\(\)", re.DOTALL)
    init_match = init_pattern.search(content)
    
    if init_match:
        # Add code to enable transaction safety at the end of the method
        init_code = init_match.group(0)
        new_init_code = init_code + "\n        # Enable transaction safety\n        DatabaseIntegration.enhance_database(self)"
        content = content[:init_match.start()] + new_init_code + content[init_match.end():]
    else:
        print("Error: Could not find _init_database method")
        return False
    
    # Create a backup of the original file
    backup_path = server_path.with_suffix(".py.bak")
    with open(backup_path, "w") as f:
        f.write(content)
    
    print(f"Created backup of server.py at {backup_path}")
    
    # Write the updated content to server.py
    with open(server_path, "w") as f:
        f.write(content)
    
    print("Transaction safety enabled in server.py")
    return True

if __name__ == "__main__":
    if enable_transaction_safety():
        print("Transaction safety has been enabled successfully")
        sys.exit(0)
    else:
        print("Failed to enable transaction safety")
        sys.exit(1)
