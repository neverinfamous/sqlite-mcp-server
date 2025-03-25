"""
Database Integration Module for SQLite MCP Server

This module integrates the transaction safety features with the 
main database class, providing a consistent interface for safe operations.
"""

import logging
from .transaction_safety import safe_execute_query

logger = logging.getLogger('mcp_sqlite_server')

class DatabaseIntegration:
    """Integration class for enhanced database operations"""
    
    @staticmethod
    def enhance_database(db_instance):
        """
        Enhance an existing database instance with transaction safety features.
        
        Args:
            db_instance: The EnhancedSqliteDatabase instance to enhance
            
        Returns:
            Enhanced database instance
        """
        # Store the original _execute_query method
        original_execute_query = db_instance._execute_query
        
        # Define a new execute query method that uses transaction safety
        def safe_execute_query_wrapper(query, params=None):
            """
            Wrapper that adds transaction safety to database operations.
            
            For write operations, this uses explicit transactions with proper rollback.
            For read operations, it passes through to the original method.
            
            Args:
                query (str): SQL query to execute
                params (dict, optional): Parameters for the query
                
            Returns:
                list: Result of query execution
            """
            logger.debug("Using safe transaction wrapper")
            
            # Use the original method for read operations and non-transactional operations
            if query.strip().upper().startswith(("SELECT", "PRAGMA")):
                return original_execute_query(query, params)
            
            # For write operations (INSERT, UPDATE, DELETE, etc.), use transaction safety
            return safe_execute_query(db_instance.db_path, query, params)
        
        # Replace the execute query method
        db_instance._execute_query = safe_execute_query_wrapper
        
        # Add a flag indicating transaction safety is enabled
        db_instance.transaction_safety_enabled = True
        
        logger.info("Transaction safety enabled for database operations")
        
        return db_instance
