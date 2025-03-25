"""
Transaction Safety Module for SQLite MCP Server

This module provides transaction safety mechanisms to protect against
interruptions during database write operations.
"""

import logging
import sqlite3
from contextlib import closing

logger = logging.getLogger('mcp_sqlite_server')

def safe_execute_query(db_path, query, params=None):
    """
    Execute a query with transaction safety guarantees.
    
    This function wraps SQL write operations in explicit BEGIN/COMMIT
    transactions to ensure atomic operations, with proper rollback
    on error or interruption.
    
    Args:
        db_path (str): Path to the SQLite database
        query (str): SQL query to execute
        params (dict, optional): Parameters for the query
        
    Returns:
        list: Result of query execution
        
    Raises:
        Exception: If query execution fails, after rolling back
    """
    logger.debug(f"Safe execution of query: {query}")
    
    # Skip transaction wrapping for read-only queries
    is_read_query = query.strip().upper().startswith("SELECT")
    
    try:
        with closing(sqlite3.connect(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            try:
                # Begin transaction for write operations
                if not is_read_query:
                    logger.debug("Beginning transaction")
                    cursor.execute("BEGIN TRANSACTION")
                
                # Execute the query
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                # Process results based on query type
                if is_read_query:
                    # For SELECT queries
                    results = [dict(row) for row in cursor.fetchall()]
                    logger.debug(f"Read query returned {len(results)} rows")
                    return results
                else:
                    # For write operations
                    conn.commit()
                    affected = cursor.rowcount
                    logger.debug(f"Write query affected {affected} rows")
                    return [{"affected_rows": affected}]
                    
            except Exception as e:
                # Roll back transaction for write operations
                if not is_read_query:
                    try:
                        logger.debug(f"Rolling back transaction due to error: {e}")
                        conn.rollback()
                    except Exception as rollback_error:
                        logger.error(f"Error during rollback: {rollback_error}")
                
                # Re-raise the original error
                raise
                
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise
