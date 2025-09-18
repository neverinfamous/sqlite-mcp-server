#!/usr/bin/env python3
"""
Standalone Test Runner for SQLite MCP Server v2.2.0

This script provides easy access to run comprehensive tests without 
requiring pytest or complex setup. It can be run directly or included
in CI/CD pipelines.

Usage:
    python test_runner.py                    # Run standard tests
    python test_runner.py --quick           # Quick smoke test  
    python test_runner.py --full            # Full comprehensive test
    python test_runner.py --check-env       # Check environment only
    python test_runner.py --version         # Show version info
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Version information
VERSION = "2.3.0"
TEST_SCRIPT = "tests/test_comprehensive.py"

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print(f"❌ Python 3.10+ required. Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are available"""
    required_modules = ["sqlite3", "json", "tempfile", "pathlib"]
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Missing required modules: {', '.join(missing)}")
        return False
    
    # Check optional dependencies
    optional_modules = {
        "numpy": "Advanced vector operations",
        "requests": "External API testing", 
        "PIL": "Spatial data testing"
    }
    
    available_optional = []
    missing_optional = []
    
    for module, description in optional_modules.items():
        try:
            __import__(module)
            available_optional.append(f"{module} ({description})")
        except ImportError:
            missing_optional.append(f"{module} ({description})")
    
    if available_optional:
        print(f"✅ Optional dependencies available: {', '.join(available_optional)}")
    
    if missing_optional:
        print(f"⚠️ Optional dependencies missing: {', '.join(missing_optional)}")
        print("   Install with: pip install -r requirements-dev.txt")
    
    return True

def find_test_script():
    """Find the comprehensive test script"""
    script_dir = Path(__file__).parent
    test_path = script_dir / TEST_SCRIPT
    
    if test_path.exists():
        return str(test_path)
    
    # Try alternative locations
    alternative_paths = [
        script_dir / "test_comprehensive.py",
        Path.cwd() / "tests" / "test_comprehensive.py",
        Path.cwd() / "test_comprehensive.py"
    ]
    
    for path in alternative_paths:
        if path.exists():
            return str(path)
    
    print(f"❌ Test script not found. Looked for:")
    print(f"   {test_path}")
    for path in alternative_paths:
        print(f"   {path}")
    
    return None

def run_environment_check():
    """Run environment compatibility check"""
    print(f"🔍 SQLite MCP Server v{VERSION} - Environment Check")
    print("=" * 50)
    
    # Python version
    if check_python_version():
        print(f"✅ Python {sys.version.split()[0]}")
    else:
        return False
    
    # Dependencies
    if not check_dependencies():
        return False
    
    # SQLite version
    try:
        import sqlite3
        sqlite_version = sqlite3.sqlite_version
        sqlite_info = sqlite3.sqlite_version_info
        jsonb_supported = sqlite_info >= (3, 45, 0)
        
        print(f"✅ SQLite {sqlite_version} ({'JSONB supported' if jsonb_supported else 'JSONB not supported'})")
        
        if not jsonb_supported:
            print("   ⚠️ Consider upgrading SQLite to 3.45+ for full JSONB support")
            
    except Exception as e:
        print(f"❌ SQLite check failed: {e}")
        return False
    
    # Test script availability
    test_script_path = find_test_script()
    if test_script_path:
        print(f"✅ Test script found: {test_script_path}")
    else:
        return False
    
    print("\n🎉 Environment check passed! Ready to run tests.")
    return True

def run_tests(test_level="standard", extra_args=None):
    """Run the comprehensive test suite"""
    if not check_python_version():
        return 1
    
    test_script_path = find_test_script()
    if not test_script_path:
        return 1
    
    # Build command
    cmd = [sys.executable, test_script_path, test_level]
    if extra_args:
        cmd.extend(extra_args)
    
    print(f"🚀 Running SQLite MCP Server Tests (Level: {test_level.upper()})")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        # Run the test script
        result = subprocess.run(cmd, check=False)
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 130
        
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return 1

def show_version():
    """Show version information"""
    print(f"SQLite MCP Server Test Runner v{VERSION}")
    print(f"Python: {sys.version}")
    
    try:
        import sqlite3
        print(f"SQLite: {sqlite3.sqlite_version}")
    except:
        print("SQLite: Not available")
    
    try:
        import mcp
        mcp_version = getattr(mcp, '__version__', 'unknown')
        print(f"MCP: {mcp_version}")
    except:
        print("MCP: Not available")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description=f"Test Runner for SQLite MCP Server v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_runner.py                # Standard tests
  python test_runner.py --quick       # Quick smoke test
  python test_runner.py --full        # Full comprehensive test
  python test_runner.py --check-env   # Environment check only
        """
    )
    
    parser.add_argument(
        "--quick", 
        action="store_const", 
        const="quick",
        dest="level",
        help="Run quick smoke test (30 seconds)"
    )
    
    parser.add_argument(
        "--standard", 
        action="store_const", 
        const="standard",
        dest="level", 
        help="Run standard test (2-3 minutes) [default]"
    )
    
    parser.add_argument(
        "--full", 
        action="store_const", 
        const="full",
        dest="level",
        help="Run full comprehensive test (5-10 minutes)"
    )
    
    parser.add_argument(
        "--check-env", 
        action="store_true",
        help="Check environment compatibility only"
    )
    
    parser.add_argument(
        "--version", 
        action="store_true",
        help="Show version information"
    )
    
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle special commands
    if args.version:
        show_version()
        return 0
    
    if args.check_env:
        return 0 if run_environment_check() else 1
    
    # Determine test level
    test_level = args.level or "standard"
    
    # Build extra arguments
    extra_args = []
    if args.verbose:
        extra_args.append("--verbose")
    
    # Run tests
    return run_tests(test_level, extra_args)

if __name__ == "__main__":
    sys.exit(main())
