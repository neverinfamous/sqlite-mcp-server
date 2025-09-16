/**
 * Safe Transaction Utilities for SQLite MCP Server
 * 
 * Provides transaction safety mechanisms to protect against
 * interruptions during write operations.
 */

/**
 * Executes a write query within an explicit transaction
 * to ensure atomic operations and proper rollback on error
 * 
 * @param {Object} db - The database connection object
 * @param {string} query - The SQL query to execute
 * @param {Array|Object} params - The parameters for the query
 * @returns {Object} The result of the query execution
 * @throws {Error} If the query fails, it will roll back and throw
 */
function safeWriteQuery(db, query, params = []) {
  try {
    // Begin transaction
    db.prepare('BEGIN TRANSACTION').run();
    
    // Execute the query
    const result = db.prepare(query).run(params);
    
    // Commit the transaction
    db.prepare('COMMIT').run();
    
    return result;
  } catch (error) {
    // Roll back on error
    try {
      db.prepare('ROLLBACK').run();
    } catch (rollbackError) {
      // Log rollback errors only if in development or debug mode
      if (process.env.NODE_ENV === 'development' || process.env.DEBUG) {
        console.error('Error during rollback:', rollbackError);
      }
    }
    
    // Rethrow the original error
    throw error;
  }
}

module.exports = {
  safeWriteQuery
};
