import sqlite3
import logging
import json
import os
from contextlib import closing
from pathlib import Path
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from pydantic import AnyUrl
from typing import Any, Dict, List, Optional, Union

from .sqlite_version import check_sqlite_version
from .jsonb_utils import convert_to_jsonb, convert_from_jsonb, validate_json
from .db_integration import DatabaseIntegration
from .error_handler import SqliteErrorHandler
from .json_logger import JsonLogger
from .schema_updater import SchemaUpdater
from .diagnostics import DiagnosticsService

# Load configuration from environment first
DEBUG_MODE = os.environ.get('SQLITE_DEBUG', 'false').lower() in ('true', '1', 'yes')

# Logging is configured by the launcher - no need to configure here
logger = logging.getLogger('mcp_sqlite_server')

# Reduce logging noise in production
if not DEBUG_MODE:
    logger.setLevel(logging.WARNING)

logger.info("Starting Enhanced MCP SQLite Server with JSONB support")
LOG_DIR = os.environ.get('SQLITE_LOG_DIR', './logs')
JSONB_ENABLED = os.environ.get('SQLITE_JSONB_ENABLED', 'true').lower() in ('true', '1', 'yes')

PROMPT_TEMPLATE = """
The assistants goal is to walkthrough an informative demo of MCP. To demonstrate the Model Context Protocol (MCP) we will leverage this example server to interact with an SQLite database.
It is important that you first explain to the user what is going on. The user has downloaded and installed the SQLite MCP Server and is now ready to use it.
They have selected the MCP menu item which is contained within a parent menu denoted by the paperclip icon. Inside this menu they selected an icon that illustrates two electrical plugs connecting. This is the MCP menu.
Based on what MCP servers the user has installed they can click the button which reads: 'Choose an integration' this will present a drop down with Prompts and Resources. The user has selected the prompt titled: 'mcp-demo'.
This text file is that prompt. The goal of the following instructions is to walk the user through the process of using the 3 core aspects of an MCP server. These are: Prompts, Tools, and Resources.
They have already used a prompt and provided a topic. The topic is: {topic}. The user is now ready to begin the demo.
Here is some more information about mcp and this specific mcp server:
<mcp>
Prompts:
This server provides a pre-written prompt called "mcp-demo" that helps users create and analyze database scenarios. The prompt accepts a "topic" argument and guides users through creating tables, analyzing data, and generating insights. For example, if a user provides "retail sales" as the topic, the prompt will help create relevant database tables and guide the analysis process. Prompts basically serve as interactive templates that help structure the conversation with the LLM in a useful way.
Resources:
This server exposes one key resource: "memo://insights", which is a business insights memo that gets automatically updated throughout the analysis process. As users analyze the database and discover insights, the memo resource gets updated in real-time to reflect new findings. Resources act as living documents that provide context to the conversation.
Tools:
This server provides several SQL-related tools:
"read_query": Executes SELECT queries to read data from the database
"write_query": Executes INSERT, UPDATE, or DELETE queries to modify data
"create_table": Creates new tables in the database
"list_tables": Shows all existing tables
"describe_table": Shows the schema for a specific table
"append_insight": Adds a new business insight to the memo resource
</mcp>
<demo-instructions>
You are an AI assistant tasked with generating a comprehensive business scenario based on a given topic.
Your goal is to create a narrative that involves a data-driven business problem, develop a database structure to support it, generate relevant queries, create a dashboard, and provide a final solution.

At each step you will pause for user input to guide the scenario creation process. Overall ensure the scenario is engaging, informative, and demonstrates the capabilities of the SQLite MCP Server.
You should guide the scenario to completion. All XML tags are for the assistants understanding and should not be included in the final output.

1. The user has chosen the topic: {topic}.

2. Create a business problem narrative:
a. Describe a high-level business situation or problem based on the given topic.
b. Include a protagonist (the user) who needs to collect and analyze data from a database.
c. Add an external, potentially comedic reason why the data hasn't been prepared yet.
d. Mention an approaching deadline and the need to use Claude (you) as a business tool to help.

3. Setup the data:
a. Instead of asking about the data that is required for the scenario, just go ahead and use the tools to create the data. Inform the user you are "Setting up the data".
b. Design a set of table schemas that represent the data needed for the business problem.
c. Include at least 2-3 tables with appropriate columns and data types.
d. Leverage the tools to create the tables in the SQLite database.
e. Create INSERT statements to populate each table with relevant synthetic data.
f. Ensure the data is diverse and representative of the business problem.
g. Include at least 10-15 rows of data for each table.

4. Pause for user input:
a. Summarize to the user what data we have created.
b. Present the user with a set of multiple choices for the next steps.
c. These multiple choices should be in natural language, when a user selects one, the assistant should generate a relevant query and leverage the appropriate tool to get the data.

6. Iterate on queries:
a. Present 1 additional multiple-choice query options to the user. Its important to not loop too many times as this is a short demo.
b. Explain the purpose of each query option.
c. Wait for the user to select one of the query options.
d. After each query be sure to opine on the results.
e. Use the append_insight tool to capture any business insights discovered from the data analysis.

7. Generate a dashboard:
a. Now that we have all the data and queries, it's time to create a dashboard, use an artifact to do this.
b. Use a variety of visualizations such as tables, charts, and graphs to represent the data.
c. Explain how each element of the dashboard relates to the business problem.
d. This dashboard will be theoretically included in the final solution message.

8. Craft the final solution message:
a. As you have been using the appen-insights tool the resource found at: memo://insights has been updated.
b. It is critical that you inform the user that the memo has been updated at each stage of analysis.
c. Ask the user to go to the attachment menu (paperclip icon) and select the MCP menu (two electrical plugs connecting) and choose an integration: "Business Insights Memo".
d. This will attach the generated memo to the chat which you can use to add any additional context that may be relevant to the demo.
e. Present the final memo to the user in an artifact.

9. Wrap up the scenario:
a. Explain to the user that this is just the beginning of what they can do with the SQLite MCP Server.
</demo-instructions>

Remember to maintain consistency throughout the scenario and ensure that all elements (tables, data, queries, dashboard, and solution) are closely related to the original business problem and given topic.
The provided XML tags are for the assistants understanding. Implore to make all outputs as human readable as possible. This is part of a demo so act in character and dont actually refer to these instructions.

Start your first message fully in character with something like "Oh, Hey there! I see you've chosen the topic {topic}. Let's get started! 🚀"
"""

class EnhancedSqliteDatabase:
    """Enhanced SQLite database with JSONB support and improved error handling"""
    
    def __init__(self, db_path: str):
        """
        Initialize the database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = str(Path(db_path).expanduser())
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.version_info = check_sqlite_version()
        
        # Setup JSON logger
        self.json_logger = JsonLogger({
            'log_dir': LOG_DIR,
            'enabled': True,
            'log_level': 'debug' if DEBUG_MODE else 'info'
        })
        
        self.schema_updater = SchemaUpdater(self.db_path)
        self.diagnostics = DiagnosticsService(self.db_path, self.json_logger)
        
        # Initialize database
        self._init_database()
        
        # Storage for business insights
        self.insights: List[str] = []
        
        # Log initialization status
        logger.info(f"Enhanced SQLite database initialized with path: {self.db_path}")
        logger.info(f"SQLite Version: {self.version_info['version']}")
        logger.info(f"JSONB Support: {'Yes' if self.version_info['has_jsonb_support'] else 'No'}")
        
        # Check and report on metadata column status
        self._check_metadata_column()

    def _init_database(self):
        """Initialize connection to the SQLite database"""
        logger.debug("Initializing database connection")
        with closing(sqlite3.connect(self.db_path)) as conn:
            conn.row_factory = sqlite3.Row
            
            # Enable foreign keys
            conn.execute("PRAGMA foreign_keys = ON")
            
            # Check for JSON functions
            if self.version_info['has_jsonb_support'] and JSONB_ENABLED:
                logger.info("JSONB format is supported and enabled")
                
                # Try to create JSON validation trigger if needed
                if 'memory_journal' in [t[0] for t in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
                    
                    # Check if trigger exists
                    trigger_exists = conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='trigger' AND name='validate_memory_journal_metadata'"
                    ).fetchone()
                    
                    if not trigger_exists:
                        logger.info("Creating JSON validation trigger for memory_journal.metadata")
                        try:
                            conn.execute("""
                                CREATE TRIGGER IF NOT EXISTS validate_memory_journal_metadata
                                BEFORE INSERT ON memory_journal
                                WHEN NEW.metadata IS NOT NULL
                                BEGIN
                                    SELECT CASE
                                        WHEN json_valid(json(NEW.metadata)) = 0
                                        THEN RAISE(ABORT, 'Invalid JSON in memory_journal.metadata')
                                    END;
                                END;
                            """)
                            conn.commit()
                            logger.info("JSON validation trigger created successfully")
                        except Exception as e:
                            logger.error(f"Failed to create JSON validation trigger: {e}")
                
            conn.close()
        # Enable transaction safety
        DatabaseIntegration.enhance_database(self)

    def _check_metadata_column(self):
        """Check if memory_journal.metadata is BLOB type for JSONB storage"""
        try:
            with closing(sqlite3.connect(self.db_path)) as conn:
                cursor = conn.cursor()
                
                # Check if memory_journal table exists
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='memory_journal'"
                )
                if not cursor.fetchone():
                    logger.info("memory_journal table does not exist yet")
                    return
                
                # Check metadata column type
                cursor.execute("PRAGMA table_info(memory_journal)")
                columns = cursor.fetchall()
                
                metadata_column = next((col for col in columns if col[1] == 'metadata'), None)
                if not metadata_column:
                    logger.info("metadata column does not exist in memory_journal table")
                    return
                
                if metadata_column[2] == 'BLOB':
                    logger.info("metadata column is already BLOB type, ready for JSONB storage")
                else:
                    logger.warning(
                        f"metadata column is {metadata_column[2]} type, not optimal for JSONB storage. "
                        f"Consider updating schema using SchemaUpdater.update_memory_journal_schema()"
                    )
                    
                    # Only try to update if JSONB is supported and enabled
                    if self.version_info['has_jsonb_support'] and JSONB_ENABLED:
                        logger.info("Attempting to update memory_journal schema for JSONB...")
                        result = self.schema_updater.update_memory_journal_schema()
                        if result.get('success', False):
                            logger.info(f"Schema updated successfully: {result}")
                        else:
                            logger.warning(f"Schema update failed: {result}")
        except Exception as e:
            logger.error(f"Failed to check metadata column: {e}")

    def _synthesize_memo(self) -> str:
        """
        Synthesize business insights into a formatted memo.
        
        Returns:
            Formatted memo as string
        """
        logger.debug(f"Synthesizing memo with {len(self.insights)} insights")
        if not self.insights:
            return "No business insights have been discovered yet."

        insights = "\n".join(f"- {insight}" for insight in self.insights)

        memo = "📊 Business Intelligence Memo 📊\n\n"
        memo += "Key Insights Discovered:\n\n"
        memo += insights

        if len(self.insights) > 1:
            memo += "\nSummary:\n"
            memo += f"Analysis has revealed {len(self.insights)} key business insights that suggest opportunities for strategic optimization and growth."

        logger.debug("Generated basic memo format")
        return memo

    def _execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a SQL query with enhanced error handling and JSONB support.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            Query results as list of dictionaries
            
        Raises:
            Exception: If query execution fails
        """
        logger.debug(f"Executing query: {query}")
        
        # Log operation for debugging
        self.json_logger.log_operation("execute_query", {
            "query": query,
            "has_params": bool(params)
        })
        
        try:
            with closing(sqlite3.connect(self.db_path)) as conn:
                conn.row_factory = sqlite3.Row
                
                # Special handling for memory_journal metadata with JSONB
                if JSONB_ENABLED and self.version_info['has_jsonb_support']:
                    # Check if it's an INSERT or UPDATE to memory_journal with metadata
                    if (
                        query.strip().upper().startswith(('INSERT', 'UPDATE')) and 
                        'memory_journal' in query and 
                        'metadata' in query
                    ):
                        # Handle JSONB conversion for memory_journal metadata
                        # This is a simplified approach - a more robust approach would use SQL parsing
                        try:
                            # For known queries we can modify them to use jsonb()
                            if (
                                ('INSERT INTO memory_journal' in query or 'UPDATE memory_journal SET' in query) and 
                                params and 
                                'metadata' in params
                            ):
                                # Check if metadata is valid JSON
                                if params['metadata']:
                                    try:
                                        validate_json(params['metadata'])
                                        
                                        # Convert to JSONB directly in the query
                                        if 'jsonb(?)' not in query:
                                            query = query.replace('metadata = ?', 'metadata = jsonb(?)')
                                    except Exception as e:
                                        logger.warning(f"Invalid JSON in metadata parameter: {e}")
                                        self.json_logger.log_error(e, {"query": query, "metadata": params['metadata']})
                        except Exception as e:
                            logger.warning(f"Failed to process JSONB conversion: {e}")
                
                # Execute the query
                with closing(conn.cursor()) as cursor:
                    try:
                        if params:
                            cursor.execute(query, params)
                        else:
                            cursor.execute(query)
                            
                        # Handle different query types
                        if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER')):
                            conn.commit()
                            affected = cursor.rowcount
                            logger.debug(f"Write query affected {affected} rows")
                            
                            # Log success
                            self.json_logger.log_operation("write_success", {
                                "affected_rows": affected,
                                "query_type": query.strip().split()[0].upper()
                            })
                            
                            return [{"affected_rows": affected}]
                        else:
                            # Handle read queries
                            results = [dict(row) for row in cursor.fetchall()]
                            
                            # Special handling for JSONB in result set
                            if JSONB_ENABLED and self.version_info['has_jsonb_support']:
                                # Check if any column in any row might be JSONB
                                for row in results:
                                    for key, value in row.items():
                                        if isinstance(value, bytes) and key == 'metadata':
                                            try:
                                                # Convert JSONB to JSON string
                                                json_str = convert_from_jsonb(conn, value)
                                                if json_str:
                                                    # Parse JSON string
                                                    row[key] = json.loads(json_str)
                                            except Exception as e:
                                                logger.warning(f"Failed to convert JSONB to JSON: {e}")
                                                # Keep as bytes if conversion fails
                            
                            logger.debug(f"Read query returned {len(results)} rows")
                            
                            # Log success
                            self.json_logger.log_operation("read_success", {
                                "rows_returned": len(results),
                                "query_type": "SELECT"
                            })
                            
                            return results
                    except Exception as e:
                        # Handle database errors with improved diagnostics
                        logger.error(f"Database error executing query: {e}")
                        
                        # Log the error with context
                        error_context = SqliteErrorHandler.extract_error_context(e, query, params)
                        error_analysis = SqliteErrorHandler.analyze_sqlite_error(e, query, params)
                        
                        self.json_logger.log_error(e, {
                            "query": query,
                            "has_params": bool(params),
                            "context": error_context,
                            "analysis": error_analysis
                        })
                        
                        # Improve the error message if it's JSON related
                        if error_analysis["is_json_related"]:
                            error_details = SqliteErrorHandler.extract_json_error_details(e, {"query": query})
                            # Create a more informative error message
                            raise type(e)(
                                f"JSON Error in query: {error_details['message']}. "
                                f"Suggestion: {error_analysis['suggestions'][0] if error_analysis['suggestions'] else 'Check JSON syntax'}"
                            )
                        
                        # Re-raise the original error
                        raise
        except Exception as e:
            # Log all errors
            logger.error(f"Error executing query: {e}")
            self.json_logger.log_error(e, {"query": query})
            raise

async def main(db_path: str):
    logger.info(f"Starting Enhanced SQLite MCP Server with DB path: {db_path}")

    # Initialize database with enhanced features
    db = EnhancedSqliteDatabase(db_path)
    
    # Check SQLite version and JSONB support
    version_info = check_sqlite_version()
    logger.info(f"SQLite Version: {version_info['version']}")
    logger.info(f"JSONB Support: {'Yes' if version_info['has_jsonb_support'] else 'No'}")
    
    # Initialize MCP server
    server = Server("sqlite-custom")

    # Register handlers
    logger.debug("Registering handlers")

    @server.list_resources()
    async def handle_list_resources() -> list[types.Resource]:
        logger.debug("Handling list_resources request")
        return [
            types.Resource(
                uri=AnyUrl("memo://insights"),
                name="Business Insights Memo",
                description="A living document of discovered business insights",
                mimeType="text/plain",
            ),
            # Add diagnostic resource
            types.Resource(
                uri=AnyUrl("diagnostics://json"),
                name="JSON Diagnostics",
                description="Diagnostic information about JSON handling capabilities",
                mimeType="application/json",
            )
        ]

    @server.read_resource()
    async def handle_read_resource(uri: AnyUrl) -> str:
        logger.debug(f"Handling read_resource request for URI: {uri}")
        
        # Handle memo resources
        if uri.scheme == "memo":
            path = str(uri).replace("memo://", "")
            if not path or path != "insights":
                logger.error(f"Unknown memo path: {path}")
                raise ValueError(f"Unknown memo path: {path}")

            return db._synthesize_memo()
            
        # Handle diagnostic resources
        elif uri.scheme == "diagnostics":
            path = str(uri).replace("diagnostics://", "")
            
            if path == "json":
                # Return JSON diagnostics as formatted string
                diagnostics = db.diagnostics.get_json_diagnostics()
                return json.dumps(diagnostics, indent=2)
            else:
                logger.error(f"Unknown diagnostics path: {path}")
                raise ValueError(f"Unknown diagnostics path: {path}")
        else:
            logger.error(f"Unsupported URI scheme: {uri.scheme}")
            raise ValueError(f"Unsupported URI scheme: {uri.scheme}")

    @server.list_prompts()
    async def handle_list_prompts() -> list[types.Prompt]:
        logger.debug("Handling list_prompts request")
        return [
            types.Prompt(
                name="mcp-demo",
                description="A prompt to seed the database with initial data and demonstrate what you can do with an SQLite MCP Server + Claude",
                arguments=[
                    types.PromptArgument(
                        name="topic",
                        description="Topic to seed the database with initial data",
                        required=True,
                    )
                ],
            ),
            # Add a diagnostic prompt
            types.Prompt(
                name="json-diagnostic",
                description="A prompt to check SQLite JSONB capabilities and run diagnostics",
                arguments=[],
            )
        ]

    @server.get_prompt()
    async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
        logger.debug(f"Handling get_prompt request for {name} with args {arguments}")
        
        if name == "mcp-demo":
            if not arguments or "topic" not in arguments:
                logger.error("Missing required argument: topic")
                raise ValueError("Missing required argument: topic")

            topic = arguments["topic"]
            prompt = PROMPT_TEMPLATE.format(topic=topic)

            logger.debug(f"Generated prompt template for topic: {topic}")
            return types.GetPromptResult(
                description=f"Demo template for {topic}",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(type="text", text=prompt.strip()),
                    )
                ],
            )
        elif name == "json-diagnostic":
            # JSON diagnostic prompt
            version_info = check_sqlite_version()
            
            diagnostic_prompt = f"""
            # SQLite JSON Capabilities Diagnostic
            
            I'd like to run a diagnostic check on your SQLite MCP server's JSON capabilities.
            
            ## System Information
            - SQLite Version: {version_info['version']}
            - JSONB Support: {"Yes" if version_info['has_jsonb_support'] else "No"}
            
            Let's use the SQLite MCP tools to run a few diagnostic tests:
            
            1. First, let's check what tables are in the database using the `list_tables` tool.
            2. If there's a memory_journal table, let's use `describe_table` to check its schema.
            3. Let's examine the JSON diagnostics resource at `diagnostics://json`.
            
            This will help us understand the JSON capabilities of your SQLite installation.
            """
            
            return types.GetPromptResult(
                description="JSON diagnostic prompt",
                messages=[
                    types.PromptMessage(
                        role="user",
                        content=types.TextContent(type="text", text=diagnostic_prompt.strip()),
                    )
                ],
            )
        else:
            logger.error(f"Unknown prompt: {name}")
            raise ValueError(f"Unknown prompt: {name}")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """List available tools"""
        basic_tools = [
            types.Tool(
                name="read_query",
                description="Execute a SELECT query on the SQLite database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "SELECT SQL query to execute"},
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="write_query",
                description="Execute an INSERT, UPDATE, or DELETE query on the SQLite database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "SQL query to execute"},
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="create_table",
                description="Create a new table in the SQLite database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "CREATE TABLE SQL statement"},
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="list_tables",
                description="List all tables in the SQLite database",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="describe_table",
                description="Get the schema information for a specific table",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {"type": "string", "description": "Name of the table to describe"},
                    },
                    "required": ["table_name"],
                },
            ),
            types.Tool(
                name="append_insight",
                description="Add a business insight to the memo",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "insight": {"type": "string", "description": "Business insight discovered from data analysis"},
                    },
                    "required": ["insight"],
                },
            ),
            # Database Administration Tools
            types.Tool(
                name="vacuum_database",
                description="Optimize database by reclaiming unused space and defragmenting",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="analyze_database",
                description="Update database statistics for query optimization",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="integrity_check",
                description="Check database integrity and report any corruption",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="database_stats",
                description="Get database performance and usage statistics",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            types.Tool(
                name="index_usage_stats",
                description="Get index usage statistics for query optimization",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
            # Full-Text Search (FTS5) Tools
            types.Tool(
                name="create_fts_table",
                description="Create a FTS5 virtual table for full-text search",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {"type": "string", "description": "Name for the FTS5 table"},
                        "columns": {"type": "array", "items": {"type": "string"}, "description": "List of columns to include in FTS5 index"},
                        "content_table": {"type": "string", "description": "Optional: source table to populate from"},
                        "tokenizer": {"type": "string", "description": "Optional: tokenizer to use (unicode61, porter, ascii)", "default": "unicode61"}
                    },
                    "required": ["table_name", "columns"],
                },
            ),
            types.Tool(
                name="rebuild_fts_index",
                description="Rebuild FTS5 index for optimal performance",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {"type": "string", "description": "Name of the FTS5 table to rebuild"},
                    },
                    "required": ["table_name"],
                },
            ),
            types.Tool(
                name="fts_search",
                description="Perform enhanced full-text search with ranking and snippets",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "table_name": {"type": "string", "description": "Name of the FTS5 table to search"},
                        "query": {"type": "string", "description": "FTS5 search query"},
                        "limit": {"type": "integer", "description": "Maximum number of results", "default": 10},
                        "snippet_length": {"type": "integer", "description": "Length of text snippets", "default": 32}
                    },
                    "required": ["table_name", "query"],
                },
            ),
        ]
        
        # Add diagnostic tools if JSONB is supported
        if db.version_info['has_jsonb_support']:
            diagnostic_tools = [
                types.Tool(
                    name="validate_json",
                    description="Validate a JSON string and provide detailed feedback",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "json_str": {"type": "string", "description": "JSON string to validate"},
                        },
                        "required": ["json_str"],
                    },
                ),
                types.Tool(
                    name="test_jsonb_conversion",
                    description="Test conversion of a JSON string to JSONB format and back",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "json_str": {"type": "string", "description": "JSON string to convert"},
                        },
                        "required": ["json_str"],
                    },
                ),
            ]
            
            return basic_tools + diagnostic_tools
        else:
            return basic_tools

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """Handle tool execution requests"""
        try:
            # Handle basic tools
            if name == "list_tables":
                results = db._execute_query(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                return [types.TextContent(type="text", text=str(results))]

            elif name == "describe_table":
                if not arguments or "table_name" not in arguments:
                    raise ValueError("Missing table_name argument")
                    
                results = db._execute_query(
                    f"PRAGMA table_info({arguments['table_name']})"
                )
                return [types.TextContent(type="text", text=str(results))]

            elif name == "append_insight":
                if not arguments or "insight" not in arguments:
                    raise ValueError("Missing insight argument")

                db.insights.append(arguments["insight"])
                _ = db._synthesize_memo()

                # Notify clients that the memo resource has changed
                await server.request_context.session.send_resource_updated(AnyUrl("memo://insights"))

                return [types.TextContent(type="text", text="Insight added to memo")]
                
            # Handle diagnostic tools
            elif name == "validate_json":
                if not arguments or "json_str" not in arguments:
                    raise ValueError("Missing json_str argument")
                    
                result = db.diagnostics.validate_json(arguments["json_str"])
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
                
            elif name == "test_jsonb_conversion":
                if not arguments or "json_str" not in arguments:
                    raise ValueError("Missing json_str argument")
                    
                result = db.diagnostics.test_jsonb_conversion(arguments["json_str"])
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]

            # Handle database administration tools
            elif name == "vacuum_database":
                logger.info("Executing VACUUM operation")
                # VACUUM must run outside of transactions, so we use a direct connection
                import sqlite3
                from contextlib import closing
                try:
                    with closing(sqlite3.connect(db.db_path)) as conn:
                        conn.execute("VACUUM")
                        conn.commit()
                    logger.info("VACUUM operation completed successfully")
                    return [types.TextContent(type="text", text="Database vacuum completed successfully")]
                except Exception as e:
                    logger.error(f"VACUUM operation failed: {e}")
                    return [types.TextContent(type="text", text=f"Database error: {str(e)}")]

            elif name == "analyze_database":
                logger.info("Executing ANALYZE operation")
                results = db._execute_query("ANALYZE")
                return [types.TextContent(type="text", text="Database analysis completed successfully")]

            elif name == "integrity_check":
                logger.info("Executing integrity check")
                results = db._execute_query("PRAGMA integrity_check")
                if results and len(results) == 1 and results[0].get('integrity_check') == 'ok':
                    return [types.TextContent(type="text", text="Database integrity check passed: OK")]
                else:
                    return [types.TextContent(type="text", text=f"Integrity check results: {str(results)}")]

            elif name == "database_stats":
                logger.info("Retrieving database statistics")
                # Collect multiple statistics
                stats = {}
                
                # Database size and page info
                page_count = db._execute_query("PRAGMA page_count")
                page_size = db._execute_query("PRAGMA page_size")
                stats['page_count'] = page_count[0]['page_count'] if page_count else 0
                stats['page_size'] = page_size[0]['page_size'] if page_size else 0
                stats['database_size_bytes'] = stats['page_count'] * stats['page_size']
                stats['database_size_mb'] = round(stats['database_size_bytes'] / (1024 * 1024), 2)
                
                # Table count
                table_count = db._execute_query("SELECT COUNT(*) as count FROM sqlite_master WHERE type='table'")
                stats['table_count'] = table_count[0]['count'] if table_count else 0
                
                # Index count  
                index_count = db._execute_query("SELECT COUNT(*) as count FROM sqlite_master WHERE type='index'")
                stats['index_count'] = index_count[0]['count'] if index_count else 0
                
                return [types.TextContent(type="text", text=json.dumps(stats, indent=2))]

            elif name == "index_usage_stats":
                logger.info("Retrieving index usage statistics")
                # Get index list and usage info
                indexes = db._execute_query("""
                    SELECT name, tbl_name, sql 
                    FROM sqlite_master 
                    WHERE type='index' AND sql IS NOT NULL
                    ORDER BY tbl_name, name
                """)
                
                return [types.TextContent(type="text", text=json.dumps(indexes, indent=2))]

            # Handle FTS5 tools
            elif name == "create_fts_table":
                logger.info(f"Creating FTS5 table: {arguments.get('table_name')}")
                table_name = arguments["table_name"]
                columns = arguments["columns"]
                content_table = arguments.get("content_table")
                tokenizer = arguments.get("tokenizer", "unicode61")
                
                # Build FTS5 CREATE statement
                columns_str = ", ".join(columns)
                fts_sql = f"CREATE VIRTUAL TABLE {table_name} USING fts5({columns_str}, tokenize='{tokenizer}')"
                
                try:
                    db._execute_query(fts_sql)
                    result_msg = f"FTS5 table '{table_name}' created successfully with columns: {columns_str}"
                    
                    # If content table specified, populate the FTS5 table
                    if content_table:
                        populate_sql = f"INSERT INTO {table_name} SELECT {columns_str} FROM {content_table}"
                        db._execute_query(populate_sql)
                        result_msg += f" and populated from '{content_table}'"
                    
                    logger.info(result_msg)
                    return [types.TextContent(type="text", text=result_msg)]
                except Exception as e:
                    error_msg = f"Failed to create FTS5 table: {str(e)}"
                    logger.error(error_msg)
                    return [types.TextContent(type="text", text=error_msg)]

            elif name == "rebuild_fts_index":
                logger.info(f"Rebuilding FTS5 index for table: {arguments.get('table_name')}")
                table_name = arguments["table_name"]
                
                try:
                    # Rebuild the FTS5 index
                    rebuild_sql = f"INSERT INTO {table_name}({table_name}) VALUES('rebuild')"
                    db._execute_query(rebuild_sql)
                    
                    result_msg = f"FTS5 index for '{table_name}' rebuilt successfully"
                    logger.info(result_msg)
                    return [types.TextContent(type="text", text=result_msg)]
                except Exception as e:
                    error_msg = f"Failed to rebuild FTS5 index: {str(e)}"
                    logger.error(error_msg)
                    return [types.TextContent(type="text", text=error_msg)]

            elif name == "fts_search":
                logger.info(f"Performing FTS5 search on table: {arguments.get('table_name')}")
                table_name = arguments["table_name"]
                query = arguments["query"]
                limit = arguments.get("limit", 10)
                snippet_length = arguments.get("snippet_length", 32)
                
                try:
                    # Enhanced FTS5 search with ranking and snippets
                    search_sql = f"""
                        SELECT *, 
                               bm25({table_name}) as rank,
                               snippet({table_name}, -1, '<mark>', '</mark>', '...', {snippet_length}) as snippet
                        FROM {table_name} 
                        WHERE {table_name} MATCH ? 
                        ORDER BY rank 
                        LIMIT ?
                    """
                    
                    results = db._execute_query(search_sql, {"query": query, "limit": limit})
                    
                    result_msg = f"Found {len(results)} results for query: '{query}'"
                    logger.info(result_msg)
                    
                    return [types.TextContent(type="text", text=json.dumps({
                        "query": query,
                        "results_count": len(results),
                        "results": results
                    }, indent=2))]
                except Exception as e:
                    error_msg = f"FTS5 search failed: {str(e)}"
                    logger.error(error_msg)
                    return [types.TextContent(type="text", text=error_msg)]

            # Handle regular query tools
            if not arguments:
                raise ValueError("Missing arguments")

            if name == "read_query":
                if not arguments["query"].strip().upper().startswith("SELECT"):
                    raise ValueError("Only SELECT queries are allowed for read_query")
                    
                results = db._execute_query(arguments["query"])
                return [types.TextContent(type="text", text=str(results))]

            elif name == "write_query":
                if arguments["query"].strip().upper().startswith("SELECT"):
                    raise ValueError("SELECT queries are not allowed for write_query")
                    
                results = db._execute_query(arguments["query"])
                return [types.TextContent(type="text", text=str(results))]

            elif name == "create_table":
                if not arguments["query"].strip().upper().startswith("CREATE TABLE"):
                    raise ValueError("Only CREATE TABLE statements are allowed")
                    
                db._execute_query(arguments["query"])
                return [types.TextContent(type="text", text="Table created successfully")]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except sqlite3.Error as e:
            # Enhanced error handling for SQLite errors
            error_context = SqliteErrorHandler.extract_error_context(e, 
                arguments.get("query", "") if arguments else "")
            error_analysis = SqliteErrorHandler.analyze_sqlite_error(e, 
                arguments.get("query", "") if arguments else "")
                
            # Format a helpful error message
            if error_analysis["is_json_related"] and error_analysis["suggestions"]:
                error_msg = f"Database error: {str(e)}\nSuggestion: {error_analysis['suggestions'][0]}"
            else:
                error_msg = f"Database error: {str(e)}"
                
            # Log the error
            db.json_logger.log_error(e, {
                "tool": name,
                "arguments": arguments,
                "error_analysis": error_analysis
            })
            
            return [types.TextContent(type="text", text=error_msg)]
            
        except Exception as e:
            # General error handling
            error_msg = f"Error: {str(e)}"
            
            # Log the error
            logger.error(f"Tool execution error: {e}")
            if hasattr(db, 'json_logger'):
                db.json_logger.log_error(e, {
                    "tool": name,
                    "arguments": arguments
                })
                
            return [types.TextContent(type="text", text=error_msg)]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="sqlite-custom",
                server_version="1.2.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )