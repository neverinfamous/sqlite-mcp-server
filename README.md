# SQLite MCP Server

*Last Updated: September 18, 2025 2:23 AM EST*

*Enterprise-grade SQLite with AI-native capabilities – v2.4.0*

[![Docker Pulls](https://img.shields.io/docker/pulls/writenotenow/sqlite-mcp-server)](https://hub.docker.com/r/writenotenow/sqlite-mcp-server)
![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-v2.4.0-green)

Transform SQLite into a powerful, AI-ready database engine with **67 specialized tools** for advanced analytics, text processing, vector search, geospatial operations, and intelligent workflow automation.

## ✅ **Quick Test - Verify Everything Works**

**NEW in v2.4.0: Test all 67 tools in 30 seconds!**

```bash
# Quick smoke test
python test_runner.py --quick

# Standard comprehensive test (recommended)
python test_runner.py --standard

# Full test suite with edge cases
python test_runner.py --full
```

**Expected output:**
```
🚀 SQLite MCP Server Comprehensive Test Suite v2.4.0
================================================================

🔍 Environment Detection:
  ✅ SQLite 3.50.2 (JSONB supported)
  ✅ Python 3.12.11  
  ✅ MCP 1.14.0

📊 Testing 67 Tools across 13 categories...

✅ Core Database Operations (8/8 passed)
✅ JSON Operations (12/12 passed)  
✅ Text Processing (8/8 passed)
🎉 SUCCESS: 63/67 tools tested successfully!
```

## 🚀 **Quick Start**

### **Option 1: Docker (Recommended)**
```bash
# Pull and run instantly
docker pull writenotenow/sqlite-mcp-server:latest

docker run -i --rm \
  -v $(pwd):/workspace \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/database.db
```

### **Option 2: Python Installation**
```bash
# Install from PyPI
pip install mcp-server-sqlite

# Or install from source
git clone https://github.com/neverinfamous/sqlite-mcp-server.git
cd sqlite-mcp-server
pip install -r requirements.txt

# Run the server
python start_sqlite_mcp.py --db-path ./database.db
```

### **Option 3: Test in 30 Seconds**
```bash
git clone https://github.com/neverinfamous/sqlite-mcp-server.git
cd sqlite-mcp-server
python test_runner.py --quick
```

### **🔥 Core Capabilities**
- 📊 **Statistical Analysis** - Descriptive stats, percentiles, time series analysis
- 🔍 **Advanced Text Processing** - Regex, fuzzy matching, phonetic search, similarity
- 🧠 **Vector/Semantic Search** - AI-native embeddings, cosine similarity, hybrid search
- 🗺️ **SpatiaLite Geospatial** - Enterprise GIS with spatial indexing and operations
- 📝 **JSONB Binary Storage** - Efficient JSON with 15% space savings and faster parsing
- 🔐 **Transaction Safety** - Auto-wrapped transactions with rollback protection
- 🎛️ **67 Specialized Tools** - Complete database administration and analytics suite

### **🏢 Enterprise Features**
- 📈 **Business Intelligence** - Integrated insights memo and workflow automation
- 🔄 **Backup/Restore** - Enterprise-grade operations with integrity verification
- 🎯 **Full-Text Search (FTS5)** - Advanced search with BM25 ranking and snippets
- 🏗️ **Virtual Tables** - Smart CSV/JSON import with automatic type inference
- ⚙️ **Advanced PRAGMA** - Complete SQLite configuration and optimization

## 📚 **MCP Client Configuration**

### **Claude Desktop**
```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "python",
      "args": ["/path/to/sqlite-mcp-server/start_sqlite_mcp.py", "--db-path", "/path/to/database.db"]
    }
  }
}
```

### **Docker with Claude Desktop**
```json
{
  "mcpServers": {
    "sqlite-mcp-server": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-v", "/path/to/project:/workspace", "writenotenow/sqlite-mcp-server:latest", "--db-path", "/workspace/database.db"]
    }
  }
}
```

## 🎨 **Usage Examples**

### **Data Analysis Workflow**
```bash
# 1. Quick validation
python test_runner.py --quick

# 2. Start with your data
python start_sqlite_mcp.py --db-path ./sales_data.db

# 3. Use with Claude/Cursor for:
#    - Statistical analysis of your datasets
#    - Text processing and pattern extraction  
#    - Vector similarity search
#    - Geospatial analysis and mapping
#    - Business intelligence insights
```

### **Docker Development**
```bash
# Development with live reload
docker run -i --rm \
  -v $(pwd):/workspace \
  -e SQLITE_DEBUG=true \
  writenotenow/sqlite-mcp-server:latest \
  --db-path /workspace/dev.db
```

## 📊 **Tool Categories**

The SQLite MCP Server provides **67 specialized tools** across **13 categories**:

| Category | Tools | Description |
|----------|-------|-------------|
| **Core Database** | 8 | CRUD operations, schema management, transactions |
| **JSON Operations** | 12 | JSONB storage, validation, extraction, modification |
| **Text Processing** | 8 | Regex, fuzzy matching, phonetic search, similarity |
| **Statistical Analysis** | 8 | Descriptive stats, percentiles, time series |
| **Full-Text Search** | 4 | FTS5 creation, indexing, BM25 ranking |
| **Vector/Semantic Search** | 6 | Embeddings, similarity, hybrid search |
| **Virtual Tables** | 6 | CSV, R-Tree, series generation |
| **Backup/Restore** | 3 | Database backup, integrity verification |
| **PRAGMA Operations** | 4 | Configuration, optimization, introspection |
| **SpatiaLite Geospatial** | 8 | Spatial indexing, geometric operations |
| **Enhanced Virtual Tables** | 4 | Smart CSV/JSON import with type inference |
| **Vector Optimization** | 4 | ANN search, clustering, performance |
| **MCP Resources/Prompts** | 4 | Meta-awareness, guided workflows |

## 🏆 **Why Choose SQLite MCP Server?**

✅ **Instantly Testable** - Validate all 67 tools in 30 seconds  
✅ **Production Ready** - Enterprise-grade testing and validation  
✅ **AI-Native** - Built specifically for LLM integration  
✅ **Comprehensive** - Everything you need in one package  
✅ **Docker Ready** - Containerized for easy deployment  
✅ **Well Documented** - Complete guides and examples  
✅ **Active Development** - Regular updates and improvements  

## 📚 **Complete Documentation**

**[→ Full Documentation & Examples](./docs/FULL-README.md)**

Comprehensive documentation including:
- **Detailed tool reference** - All 67 tools with examples
- **Advanced configuration** - Performance tuning and optimization
- **Integration guides** - MCP clients, Docker, CI/CD
- **Feature deep-dives** - Text processing, vector search, geospatial
- **Best practices** - Query patterns, troubleshooting, workflows
- **API reference** - Complete tool schemas and parameters

## 🔗 **Additional Resources**

- **[Testing Guide](./tests/README.md)** - Comprehensive testing documentation
- **[Contributing](./CONTRIBUTING.md)** - How to contribute to the project
- **[Security Policy](./SECURITY.md)** - Security guidelines and reporting
- **[Code of Conduct](./CODE_OF_CONDUCT.md)** - Community guidelines
- **[Docker Hub](https://hub.docker.com/r/writenotenow/sqlite-mcp-server)** - Container images
- **[GitHub Releases](https://github.com/neverinfamous/sqlite-mcp-server/releases)** - Version history

## 🚀 **Quick Links**

| Action | Command |
|--------|---------|
| **Test Everything** | `python test_runner.py --standard` |
| **Docker Quick Start** | `docker run -i --rm -v $(pwd):/workspace writenotenow/sqlite-mcp-server:latest` |
| **Install from PyPI** | `pip install mcp-server-sqlite` |
| **View Full Docs** | [docs/FULL-README.md](./docs/FULL-README.md) |
| **Report Issues** | [GitHub Issues](https://github.com/neverinfamous/sqlite-mcp-server/issues) |

## 📈 **Project Stats**

- **67 Tools** across 13 categories
- **2,000+ lines** of comprehensive documentation  
- **Multi-platform** support (Windows, Linux, macOS)
- **Docker images** for amd64 and arm64
- **Enterprise testing** with comprehensive validation
- **Active development** with regular updates