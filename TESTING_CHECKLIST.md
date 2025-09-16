# SQLite MCP Server - Comprehensive Testing Checklist

*Version 1.0 - Created September 16, 2025*

## Pre-Test Setup

- [ ] Ensure Desktop Commander is initialized with all tools
- [ ] Verify Git authentication is working
- [ ] Clean up any existing test databases
- [ ] Note current working directory and database paths

## 1. Basic Database Operations

### 1.1 Database Creation & Connection
- [ ] Create new database in project root: `./test-new.db`
- [ ] Create new database in subdirectory: `./data/test-subdir.db`
- [ ] Create new database with absolute path
- [ ] Connect to existing database
- [ ] Verify database file creation on disk

### 1.2 Table Operations
- [ ] `list_tables` - Get all tables
- [ ] `create_table` - Create new table with various column types
- [ ] `describe_table` - Get table schema
- [ ] Create table with foreign key constraints
- [ ] Create table with JSON column

### 1.3 Basic CRUD Operations
- [ ] `write_query` INSERT - Single record
- [ ] `write_query` INSERT - Multiple records  
- [ ] `read_query` SELECT - Simple query
- [ ] `read_query` SELECT - With WHERE clause
- [ ] `write_query` UPDATE - Single record
- [ ] `write_query` UPDATE - Multiple records
- [ ] `write_query` DELETE - Single record
- [ ] `write_query` DELETE - Multiple records

## 2. Parameter Binding Tests

### 2.1 Read Query Parameter Binding
- [ ] SELECT with single ? parameter (string)
- [ ] SELECT with single ? parameter (integer)
- [ ] SELECT with single ? parameter (boolean)
- [ ] SELECT with multiple ? parameters
- [ ] SELECT with NULL parameter
- [ ] Complex query with multiple WHERE conditions using parameters

### 2.2 Write Query Parameter Binding
- [ ] INSERT with single ? parameter
- [ ] INSERT with multiple ? parameters
- [ ] INSERT with mixed data types (string, int, float, boolean, null)
- [ ] UPDATE with ? parameters in SET and WHERE clauses
- [ ] DELETE with ? parameters in WHERE clause
- [ ] Batch INSERT with multiple parameter sets

### 2.3 Parameter Binding Edge Cases
- [ ] Empty string parameter
- [ ] Very long string parameter
- [ ] Special characters in parameters (quotes, backslashes, unicode)
- [ ] SQL injection attempt via parameters (should be prevented)
- [ ] Wrong number of parameters (should error gracefully)

## 3. JSON Operations

### 3.1 JSON Storage
- [ ] Insert JSON string directly
- [ ] Insert JSON via parameter binding
- [ ] Insert complex nested JSON
- [ ] Insert JSON array
- [ ] Insert malformed JSON (should error)

### 3.2 JSON Querying
- [ ] `json_extract()` - Simple key extraction
- [ ] `json_extract()` - Nested key extraction
- [ ] `json_extract()` - Array element access
- [ ] Filter records by JSON field value
- [ ] Filter with JSON field via parameter binding

### 3.3 JSONB Binary Storage
- [ ] Verify JSONB format is used internally
- [ ] Compare storage efficiency vs text JSON
- [ ] Test `json_valid()` function
- [ ] Test JSON modification functions (`json_set`, `json_insert`, `json_remove`)

### 3.4 JSON Escaping & Special Characters
- [ ] JSON with quotes and backslashes
- [ ] JSON with unicode characters
- [ ] JSON with newlines and tabs
- [ ] Very large JSON objects
- [ ] Empty JSON objects and arrays

## 4. Advanced Features

### 4.1 Transaction Safety
- [ ] Successful transaction commits properly
- [ ] Failed transaction rolls back completely
- [ ] Interruption handling (if testable)
- [ ] Foreign key constraint enforcement
- [ ] Multiple operations in single transaction

### 4.2 Schema Operations
- [ ] ALTER TABLE operations
- [ ] DROP TABLE operations
- [ ] CREATE INDEX operations
- [ ] PRAGMA operations
- [ ] Database integrity checks

### 4.3 Full-Text Search (if available)
- [ ] FTS table creation
- [ ] FTS indexing
- [ ] FTS querying with MATCH
- [ ] FTS ranking and snippets

## 5. Maintenance & Monitoring

### 5.1 Insights & Memo System
- [ ] `append_insight` - Add single insight
- [ ] `append_insight` - Add multiple insights
- [ ] Verify memo resource updates
- [ ] Check memo formatting and content

### 5.2 Notification System
- [ ] Check existing notifications
- [ ] Verify notification types and severity levels
- [ ] Test notification content parsing
- [ ] Check notification timestamps

### 5.3 Integrity Monitoring
- [ ] Run integrity checks
- [ ] Check foreign key violations
- [ ] Verify maintenance logging
- [ ] Test repair capabilities (if available)

## 6. Multi-Database Support

### 6.1 Database Path Flexibility
- [ ] Use relative path: `./database.db`
- [ ] Use absolute path: `/full/path/to/database.db`
- [ ] Use subdirectory: `./data/database.db`
- [ ] Auto-create parent directories
- [ ] Handle non-existent paths gracefully

### 6.2 Database Switching
- [ ] Connect to Database A
- [ ] Perform operations on Database A
- [ ] Connect to Database B
- [ ] Perform operations on Database B
- [ ] Verify data isolation between databases

### 6.3 Special Database Types
- [ ] In-memory database (`:memory:`)
- [ ] Temporary database
- [ ] Read-only database (if supported)

## 7. Error Handling & Edge Cases

### 7.1 SQL Errors
- [ ] Syntax errors in queries
- [ ] Table/column not found errors
- [ ] Data type mismatch errors
- [ ] Constraint violation errors
- [ ] Permission errors (if applicable)

### 7.2 Parameter Errors
- [ ] Missing required parameters
- [ ] Wrong parameter count
- [ ] Invalid parameter types
- [ ] NULL handling in parameters

### 7.3 Database Errors
- [ ] Database file not found
- [ ] Database file corrupted
- [ ] Database locked by another process
- [ ] Insufficient disk space (if testable)

## 8. Performance & Limits

### 8.1 Data Volume
- [ ] Insert 1,000 records
- [ ] Insert 10,000 records (if feasible)
- [ ] Query large datasets
- [ ] Large JSON documents
- [ ] Very long text fields

### 8.2 Query Complexity
- [ ] Complex JOINs
- [ ] Subqueries
- [ ] Window functions
- [ ] Aggregate functions with GROUP BY
- [ ] Multiple table operations

## 9. Cleanup & Verification

### 9.1 Database Cleanup
- [ ] Delete test databases created during testing
- [ ] Verify no test data in production databases
- [ ] Clean up temporary files
- [ ] Check disk space usage

### 9.2 State Verification
- [ ] Verify original database state unchanged
- [ ] Check for memory leaks (if applicable)
- [ ] Verify no hanging connections
- [ ] Check log files for errors

## 10. Documentation Updates

- [ ] Record any failures or issues found
- [ ] Update README.md with verified capabilities
- [ ] Update troubleshooting section with solutions
- [ ] Document any limitations discovered
- [ ] Update version information

---

## Test Results Template

**Test Date**: 
**Tester**: 
**Environment**: 
**Database Version**: 
**MCP Server Version**: 

### Summary
- **Total Tests**: 
- **Passed**: 
- **Failed**: 
- **Skipped**: 

### Critical Issues Found
1. 
2. 
3. 

### Minor Issues Found
1. 
2. 
3. 

### Performance Notes
- 
- 

### Recommendations
- 
- 

**Overall Status**: [ ] PASS [ ] FAIL [ ] NEEDS WORK