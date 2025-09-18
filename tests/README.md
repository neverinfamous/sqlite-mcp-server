# SQLite MCP Server Test Suite

This directory contains comprehensive tests for the SQLite MCP Server v2.3.0, covering all 67 tools across 13 feature categories.

## Quick Start

**Test everything in 30 seconds:**
```bash
python test_runner.py --quick
```

**Run from tests directory:**
```bash
python test_comprehensive.py --standard
```

## Test Structure

### Comprehensive Testing (`test_comprehensive.py`)
- **Purpose**: End-to-end validation of all 67 MCP tools
- **Coverage**: Core DB, JSON, Text Processing, Vector Search, Spatial, etc.
- **Levels**: Quick (30s), Standard (2-3min), Full (5-10min)
- **Smart Environment Detection**: Auto-detects capabilities and skips unavailable features

### Existing Focused Tests
- `test_basic.py` - Basic functionality and imports
- `test_json_operations.py` - Detailed JSON/JSONB operations
- `test_transaction_safety.py` - Transaction safety mechanisms
- `test_foreign_keys.py` - Foreign key constraint testing
- `test_parameter_binding.py` - SQL parameter binding
- `test_multi_database.py` - Multi-database operations

### Integration Testing (`test_integration.py`)
- Ensures comprehensive tests work alongside existing tests
- Validates pytest compatibility
- Verifies test runner functionality

## Test Levels

### 🚀 Quick (30 seconds)
```bash
python test_runner.py --quick
```
- Core database operations
- Basic JSON functionality
- Environment detection
- **Use case**: CI/CD smoke tests, quick validation

### ⚡ Standard (2-3 minutes) [Recommended]
```bash
python test_runner.py --standard
```
- All core features
- Advanced JSON/text processing
- Vector operations (basic)
- Statistical analysis
- **Use case**: Pre-deployment validation, development testing

### 🔬 Full (5-10 minutes)
```bash
python test_runner.py --full
```
- All 67 tools
- Edge cases and error conditions
- Performance validation
- Complex nested operations
- **Use case**: Release validation, comprehensive verification

## Environment Detection

The test suite automatically detects your environment:

```
🔍 Environment Detection:
  ✅ SQLite 3.50.2 (JSONB supported)
  ✅ Python 3.12.11  
  ✅ MCP 1.14.0
  ⚠️ SpatiaLite not available (skipping geospatial tests)
```

**Features tested based on availability:**
- ✅ **Always**: Core DB, JSON, Text Processing, Statistics
- ✅ **SQLite 3.45+**: JSONB binary storage
- ⚠️ **Optional**: SpatiaLite geospatial (platform-dependent)
- ⚠️ **Optional**: Advanced vector operations (numpy)

## Running Tests

### Standalone Test Runner (Recommended)
```bash
# Quick validation
python test_runner.py --quick

# Standard comprehensive test  
python test_runner.py --standard

# Full test suite
python test_runner.py --full

# Environment check only
python test_runner.py --check-env
```

### Direct Test Execution
```bash
# Run comprehensive tests directly
python tests/test_comprehensive.py --standard

# Run with pytest
pytest tests/test_comprehensive.py

# Run all existing tests
pytest tests/
```

### CI/CD Integration
```bash
# Quick validation for CI
python test_runner.py --quick

# Exit code 0 = success, 1 = failure
echo $?
```

## Test Categories

The comprehensive test suite covers these categories:

1. **Core Database** (8 tools) - CRUD, schema, transactions
2. **JSON Operations** (12 tools) - JSONB, validation, extraction
3. **Text Processing** (8 tools) - Regex, fuzzy matching, similarity
4. **Statistical Analysis** (8 tools) - Descriptive stats, percentiles
5. **Full-Text Search** (4 tools) - FTS5 creation, indexing, search
6. **Vector/Semantic Search** (6 tools) - Embeddings, similarity, hybrid
7. **Virtual Tables** (6 tools) - CSV, R-Tree, series generation
8. **Backup/Restore** (3 tools) - Database backup, integrity
9. **PRAGMA Operations** (4 tools) - Configuration, optimization
10. **SpatiaLite Geospatial** (8 tools) - Spatial indexing, operations
11. **Enhanced Virtual Tables** (4 tools) - Smart CSV/JSON import
12. **Vector Optimization** (4 tools) - ANN search, clustering
13. **MCP Resources/Prompts** (4 tools) - Meta-awareness features

## Expected Results

### ✅ Success (95%+ pass rate)
```
🎉 EXCELLENT: 63/67 tools tested successfully!
💡 Your SQLite MCP Server is ready for production use!
```

### ⚠️ Partial Success (80-95% pass rate)
```
✅ GOOD: 58/67 tools tested successfully!
⚠️ 4 tools skipped due to missing dependencies
💡 Consider installing optional dependencies for full functionality
```

### ❌ Issues Detected (<80% pass rate)
```
⚠️ NEEDS ATTENTION: 45/67 tools tested successfully!
❌ FAILED TESTS:
  • JSON Operations: jsonb_operations - JSONB not supported
💡 Check your SQLite version and dependencies
```

## Dependencies

### Required (Always)
- Python 3.10+
- SQLite 3.0+ (3.45+ recommended for JSONB)
- MCP 1.14.0+

### Optional (Enhanced Features)
```bash
# Install optional dependencies
pip install -r requirements-dev.txt
```

- **numpy** - Vector operations testing (~15MB)
- **requests** - External API testing (~500KB)
- **Pillow** - Spatial data testing (~3MB)

**Total additional size: ~18MB** (well under the 15MB target)

## Integration with Existing Tests

The comprehensive test suite **complements** rather than **replaces** existing tests:

- **Existing tests**: Focused, detailed testing of specific features
- **Comprehensive tests**: End-to-end validation of all tools working together
- **Integration tests**: Ensure both approaches work seamlessly

Run both for maximum confidence:
```bash
# Run existing focused tests
pytest tests/test_*.py

# Run comprehensive validation  
python test_runner.py --standard
```

## Troubleshooting

### Common Issues

**"Test script not found"**
```bash
# Ensure you're in the project root
cd /path/to/sqlite-mcp-server
python test_runner.py
```

**"Module not found"**
```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # optional
```

**"SQLite version too old"**
- Some features require SQLite 3.45+ for JSONB support
- Tests will skip unsupported features gracefully

**"SpatiaLite not available"**
- Geospatial tests will be skipped automatically
- Install SpatiaLite extension for full spatial functionality

### Getting Help

If tests fail unexpectedly:

1. Run environment check: `python test_runner.py --check-env`
2. Try quick test first: `python test_runner.py --quick`
3. Check dependencies: `pip list | grep -E "(mcp|sqlite|numpy)"`
4. Review failed test details in the output

## Contributing

When adding new tools to the server:

1. Add corresponding tests to `test_comprehensive.py`
2. Update the tool count in comments and documentation
3. Run full test suite: `python test_runner.py --full`
4. Ensure all existing tests still pass: `pytest tests/`

The comprehensive test suite makes it easy to verify that new features work correctly and don't break existing functionality.
