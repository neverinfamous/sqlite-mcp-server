#!/usr/bin/env python3
"""
Integration Test - Shows how comprehensive tests work with existing tests

This test demonstrates that the new comprehensive test suite integrates
seamlessly with the existing pytest-based test infrastructure.
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

def test_existing_tests_still_work():
    """Verify existing test infrastructure still works"""
    # Import from existing tests to ensure compatibility
    try:
        from test_basic import test_import_server, test_sqlite_version
        
        # Run existing tests
        test_import_server()
        test_sqlite_version()
        
        assert True, "Existing tests run successfully"
        
    except ImportError:
        pytest.skip("Existing test modules not available")

def test_comprehensive_test_available():
    """Verify comprehensive test script is available"""
    comprehensive_test_path = Path(__file__).parent / "test_comprehensive.py"
    
    assert comprehensive_test_path.exists(), "Comprehensive test script should exist"
    
    # Verify it's importable
    try:
        sys.path.insert(0, str(comprehensive_test_path.parent))
        import test_comprehensive
        
        # Verify main class exists
        assert hasattr(test_comprehensive, 'ComprehensiveTestSuite'), "ComprehensiveTestSuite class should exist"
        
        # Verify test runner exists
        test_runner_path = Path(__file__).parent.parent / "test_runner.py"
        assert test_runner_path.exists(), "Test runner script should exist"
        
    except ImportError as e:
        pytest.fail(f"Could not import comprehensive test: {e}")

def test_comprehensive_test_can_run():
    """Test that comprehensive test suite can be instantiated"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from test_comprehensive import ComprehensiveTestSuite
        
        # Create test suite
        suite = ComprehensiveTestSuite("quick")
        
        # Verify configuration
        assert suite.test_level == "quick"
        assert "description" in suite.config
        assert "timeout" in suite.config
        
        # Verify methods exist
        assert hasattr(suite, 'setup_test_database')
        assert hasattr(suite, 'detect_environment')
        assert hasattr(suite, 'run_all_tests')
        
    except Exception as e:
        pytest.fail(f"Could not create comprehensive test suite: {e}")

def test_test_levels_configured():
    """Test that all test levels are properly configured"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from test_comprehensive import ComprehensiveTestSuite
        
        # Test all levels
        for level in ["quick", "standard", "full"]:
            suite = ComprehensiveTestSuite(level)
            
            assert suite.test_level == level
            assert suite.config["timeout"] > 0
            assert suite.config["sample_size"] > 0
            assert "description" in suite.config
            
    except Exception as e:
        pytest.fail(f"Test level configuration failed: {e}")

if __name__ == "__main__":
    pytest.main([__file__])
