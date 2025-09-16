"""SQLite error handling utilities"""

class SqliteErrorHandler:
    """Handle SQLite errors with enhanced diagnostics"""
    
    @staticmethod
    def extract_error_context(error, query, params=None):
        """Extract error context from SQLite error"""
        return {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'query': query[:100] if query else None,
            'has_params': bool(params)
        }
    
    @staticmethod
    def analyze_sqlite_error(error, query, params=None):
        """Analyze SQLite error and provide suggestions"""
        error_msg = str(error).lower()
        
        is_json_related = any(keyword in error_msg for keyword in [
            'json', 'jsonb', 'invalid', 'malformed'
        ])
        
        suggestions = []
        if is_json_related:
            suggestions.append("Check JSON syntax - ensure proper quotes and structure")
        
        return {
            'is_json_related': is_json_related,
            'suggestions': suggestions,
            'error_category': 'json' if is_json_related else 'general'
        }
    
    @staticmethod
    def extract_json_error_details(error, context):
        """Extract JSON-specific error details"""
        return {
            'message': str(error),
            'context': context,
            'type': 'json_error'
        }