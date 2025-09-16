# Contributing to SQLite MCP Server

Thank you for your interest in contributing to the SQLite MCP Server! We welcome contributions from everyone, whether you're fixing a bug, adding a feature, or improving documentation.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- SQLite 3.45.0+ (for JSONB support)
- Git
- A GitHub account

### Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp_server_sqlite.git
   cd mcp_server_sqlite
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt  # If it exists
   ```

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, please include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, SQLite version)
- Any relevant error messages or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- A clear and descriptive title
- A detailed description of the proposed feature
- Use cases that would benefit from this enhancement
- Any relevant examples or mockups

### Pull Requests

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Add or update tests as needed
4. Ensure all tests pass:
   ```bash
   python -m pytest
   ```
5. Update documentation if necessary
6. Commit your changes with a clear commit message:
   ```bash
   git commit -m "Add feature: brief description of what you added"
   ```
7. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
8. Create a Pull Request on GitHub

### Code Style

- Follow PEP 8 for Python code style
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and reasonably sized
- Use type hints where appropriate

### Testing

- Write tests for new features and bug fixes
- Ensure existing tests continue to pass
- Test with different SQLite versions when possible
- Include edge cases in your tests

### Documentation

- Update the README.md if your changes affect usage
- Add docstrings to new functions and classes
- Update any relevant documentation files
- Consider adding examples for new features

## Development Guidelines

### Database Operations

- Always use parameterized queries to prevent SQL injection
- Handle database errors gracefully
- Use transactions for multi-step operations
- Test with both empty and populated databases

### MCP Integration

- Follow MCP protocol specifications
- Ensure tools have clear descriptions and proper schemas
- Handle MCP errors appropriately
- Test with different MCP clients when possible

### Performance Considerations

- Be mindful of query performance, especially for large datasets
- Use appropriate SQLite features (indexes, JSONB, etc.)
- Consider memory usage for large result sets
- Profile performance-critical code paths

## Community

- Be respectful and inclusive in all interactions
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md)
- Help others learn and contribute
- Share knowledge and best practices

## Questions?

If you have questions about contributing, feel free to:

- Open an issue for discussion
- Contact the maintainers at writenotenow@gmail.com

Thank you for contributing to making the SQLite MCP Server better for everyone!
