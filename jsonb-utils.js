/**
 * JSONB Utilities for SQLite MCP Server
 * 
 * IMPORTANT: These JavaScript utilities are OPTIONAL helper functions.
 * The main SQLite MCP Server is Python-based and works without these utilities.
 * 
 * These utilities are designed for advanced users who want to work with JSONB 
 * binary format in SQLite 3.45.0+ using Node.js. They require better-sqlite3
 * which needs native compilation.
 * 
 * For most users: Just use the Python MCP server directly - no JavaScript needed!
 * 
 * @module jsonb-utils
 */

// Note: This utility requires better-sqlite3 for database operations
// Install with: npm install better-sqlite3 (requires Visual Studio C++ tools on Windows)
// Alternative: Use the Python MCP server which handles SQLite operations natively

/**
 * Validates if SQLite version supports JSONB
 * Requires SQLite 3.45.0+
 * 
 * @param {Object} db - Database instance (better-sqlite3 compatible)
 * @returns {Object} Version information and support status
 */
function checkJsonbSupport(db) {
  const result = db.prepare('SELECT sqlite_version() as version').get();
  const version = result.version;
  
  const versionParts = version.split('.').map(part => parseInt(part, 10));
  const hasJsonbSupport = 
    versionParts[0] > 3 || 
    (versionParts[0] === 3 && versionParts[1] >= 45);
  
  return {
    version,
    hasJsonbSupport,
    versionParts
  };
}

/**
 * Validates JSON string format
 * 
 * @param {string} jsonString - JSON string to validate
 * @returns {Object} Validation result with details
 */
function validateJson(jsonString) {
  if (!jsonString) {
    return {
      valid: false,
      error: 'Empty JSON string',
      errorType: 'EmptyInput'
    };
  }
  
  try {
    // Attempt to parse the JSON
    const parsed = JSON.parse(jsonString);
    
    return {
      valid: true,
      parsed
    };
  } catch (error) {
    // Extract position from error message if available
    const positionMatch = error.message.match(/position (\d+)/);
    const position = positionMatch ? parseInt(positionMatch[1], 10) : null;
    
    // Create helpful error context
    let errorContext = null;
    if (position !== null) {
      const start = Math.max(0, position - 20);
      const end = Math.min(jsonString.length, position + 20);
      errorContext = jsonString.substring(start, end);
    }
    
    return {
      valid: false,
      error: error.message,
      errorType: error.name,
      position,
      errorContext
    };
  }
}

/**
 * Creates JSON validation triggers for a table
 * 
 * @param {Object} db - Database instance (better-sqlite3 compatible) 
 * @param {string} tableName - Name of the table
 * @param {string} columnName - Name of the JSON column
 * @returns {Object} Result of trigger creation
 */
function createJsonValidationTriggers(db, tableName, columnName) {
  const results = { created: [] };
  
  try {
    // Create trigger for INSERT operations
    const insertTriggerName = `validate_${tableName}_${columnName}_insert`;
    db.prepare(`
      CREATE TRIGGER IF NOT EXISTS ${insertTriggerName}
      BEFORE INSERT ON ${tableName}
      FOR EACH ROW
      WHEN NEW.${columnName} IS NOT NULL AND NOT json_valid(NEW.${columnName})
      BEGIN
        SELECT RAISE(ABORT, 'Invalid JSON in ${columnName}');
      END;
    `).run();
    results.created.push(insertTriggerName);
    
    // Create trigger for UPDATE operations
    const updateTriggerName = `validate_${tableName}_${columnName}_update`;
    db.prepare(`
      CREATE TRIGGER IF NOT EXISTS ${updateTriggerName}
      BEFORE UPDATE OF ${columnName} ON ${tableName}
      FOR EACH ROW
      WHEN NEW.${columnName} IS NOT NULL AND NOT json_valid(NEW.${columnName