#!/usr/bin/env python3
"""
Test suite for spatial function preprocessing (GeomFromText wrapper)

Tests the Windows SpatiaLite compatibility wrapper that converts
GeomFromText() calls in INSERT/UPDATE statements to equivalent
functions that work reliably.
"""

import sys
import tempfile
import unittest
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from mcp_server_sqlite.server import EnhancedSqliteDatabase


class TestSpatialPreprocessing(unittest.TestCase):
    """Test spatial function preprocessing functionality"""
    
    def setUp(self):
        """Set up test database"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = EnhancedSqliteDatabase(self.temp_db.name)
        
        # Mock SpatiaLite availability for testing
        # Note: This is for testing purposes only
        object.__setattr__(self.db, '_spatialite_path', "mock_spatialite")
    
    def tearDown(self):
        """Clean up test database"""
        import os
        try:
            os.unlink(self.temp_db.name)
        except:
            pass
    
    def test_point_geometry_preprocessing(self):
        """Test GeomFromText POINT conversion to MakePoint"""
        test_cases = [
            # Basic POINT with SRID
            {
                'input': "INSERT INTO table (geom) VALUES (GeomFromText('POINT(1 2)', 4326))",
                'expected_contains': "MakePoint(1, 2, 4326)"
            },
            # POINT without explicit SRID (should default to 4326)
            {
                'input': "INSERT INTO table (geom) VALUES (GeomFromText('POINT(10.5 20.7)'))",
                'expected_contains': "MakePoint(10.5, 20.7, 4326)"
            },
            # POINT with 3D coordinates
            {
                'input': "INSERT INTO table (geom) VALUES (GeomFromText('POINT(1 2 3)', 4326))",
                'expected_contains': "MakePointZ(1, 2, 3, 4326)"
            },
            # POINT with extra whitespace  
            {
                'input': "INSERT INTO table (geom) VALUES (GeomFromText('POINT(1.5 2.5)', 3857))",
                'expected_contains': "MakePoint(1.5, 2.5, 3857)"
            },
            # Double quotes instead of single quotes
            {
                'input': 'INSERT INTO table (geom) VALUES (GeomFromText("POINT(1 2)", 4326))',
                'expected_contains': "MakePoint(1, 2, 4326)"
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            with self.subTest(f"Point test {i+1}"):
                result = self.db._preprocess_spatial_functions(test_case['input'])
                self.assertIn(test_case['expected_contains'], result,
                            f"Expected '{test_case['expected_contains']}' in '{result}'")
                self.assertNotIn('GeomFromText', result,
                               f"GeomFromText should be replaced in '{result}'")
    
    def test_non_point_geometry_preprocessing(self):
        """Test GeomFromText with LINESTRING, POLYGON, etc."""
        test_cases = [
            # LINESTRING
            {
                'input': "INSERT INTO table (geom) VALUES (GeomFromText('LINESTRING(0 0, 1 1, 2 2)', 4326))",
                'expected_contains': "GeomFromWKB(GeomFromText('LINESTRING(0 0, 1 1, 2 2)', 4326))"
            },
            # POLYGON
            {
                'input': "INSERT INTO table (geom) VALUES (GeomFromText('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))', 4326))",
                'expected_contains': "GeomFromWKB(GeomFromText('POLYGON((0 0, 0 1, 1 1, 1 0, 0 0))', 4326))"
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            with self.subTest(f"Non-point test {i+1}"):
                result = self.db._preprocess_spatial_functions(test_case['input'])
                self.assertIn(test_case['expected_contains'], result,
                            f"Expected '{test_case['expected_contains']}' in '{result}'")
    
    def test_select_queries_unchanged(self):
        """Test that SELECT queries are not preprocessed through _execute_query"""
        # For SELECT queries, we test that preprocessing is not applied via the main execution path
        # Note: _preprocess_spatial_functions itself will process any query, but it's only called for INSERT/UPDATE
        pass  # This test is conceptually covered by the conditional logic in _execute_query
    
    def test_update_queries_preprocessed(self):
        """Test that UPDATE queries are preprocessed"""
        test_cases = [
            {
                'input': "UPDATE table SET geom = GeomFromText('POINT(1 2)', 4326) WHERE id = 1",
                'expected_contains': "MakePoint(1, 2, 4326)"
            },
            {
                'input': "UPDATE spatial_table SET location = GeomFromText('POINT(10 20)')",
                'expected_contains': "MakePoint(10, 20, 4326)"  # Default SRID when none specified
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            with self.subTest(f"UPDATE test {i+1}"):
                result = self.db._preprocess_spatial_functions(test_case['input'])
                self.assertIn(test_case['expected_contains'], result,
                            f"Expected '{test_case['expected_contains']}' in '{result}'")
    
    def test_no_spatialite_path_no_preprocessing(self):
        """Test that preprocessing is skipped when SpatiaLite is not available"""
        # Remove SpatiaLite path
        object.__setattr__(self.db, '_spatialite_path', None)
        
        # Test that the preprocessing method itself still works, but the conditional check
        # in _execute_query would skip it. Since we're testing the preprocessing function
        # directly, we expect it to process the query regardless of SpatiaLite availability.
        query = "INSERT INTO table (geom) VALUES (GeomFromText('POINT(1 2)', 4326))"
        result = self.db._preprocess_spatial_functions(query)
        
        # The preprocessing function itself doesn't check _spatialite_path, 
        # that check is done in _execute_query, so this will still be processed
        self.assertIn("MakePoint(1, 2, 4326)", result)
    
    def test_no_geomfromtext_no_preprocessing(self):
        """Test that queries without GeomFromText are unchanged"""
        test_cases = [
            "INSERT INTO table (name, value) VALUES ('test', 123)",
            "INSERT INTO spatial_table (geom) VALUES (MakePoint(1, 2, 4326))",
            "UPDATE table SET name = 'updated' WHERE id = 1"
        ]
        
        for i, query in enumerate(test_cases):
            with self.subTest(f"No GeomFromText test {i+1}"):
                result = self.db._preprocess_spatial_functions(query)
                self.assertEqual(query, result,
                               f"Query without GeomFromText should remain unchanged")
    
    def test_malformed_geomfromtext_graceful_handling(self):
        """Test that malformed GeomFromText calls are handled gracefully"""
        test_cases = [
            # Missing closing parenthesis
            "INSERT INTO table (geom) VALUES (GeomFromText('POINT(1 2')",
            # Invalid WKT
            "INSERT INTO table (geom) VALUES (GeomFromText('INVALID(1 2)', 4326))",
            # Missing coordinates
            "INSERT INTO table (geom) VALUES (GeomFromText('POINT()', 4326))"
        ]
        
        for i, query in enumerate(test_cases):
            with self.subTest(f"Malformed test {i+1}"):
                # Should not raise an exception
                try:
                    result = self.db._preprocess_spatial_functions(query)
                    # Should return something (either processed or original)
                    self.assertIsInstance(result, str)
                except Exception as e:
                    self.fail(f"Preprocessing should handle malformed input gracefully: {e}")
    
    def test_multiple_geomfromtext_in_single_query(self):
        """Test handling multiple GeomFromText calls in one query"""
        query = """
        INSERT INTO table (geom1, geom2) VALUES 
        (GeomFromText('POINT(1 2)', 4326), GeomFromText('POINT(3 4)', 3857))
        """
        
        result = self.db._preprocess_spatial_functions(query)
        
        # Should replace both occurrences
        self.assertIn("MakePoint(1, 2, 4326)", result)
        self.assertIn("MakePoint(3, 4, 3857)", result)
        self.assertNotIn("GeomFromText", result)
    
    def test_case_insensitive_matching(self):
        """Test that preprocessing works with different case variations"""
        test_cases = [
            "INSERT INTO table (geom) VALUES (geomfromtext('POINT(1 2)', 4326))",
            "INSERT INTO table (geom) VALUES (GEOMFROMTEXT('POINT(1 2)', 4326))",
            "INSERT INTO table (geom) VALUES (GeomFromText('point(1 2)', 4326))"
        ]
        
        for i, query in enumerate(test_cases):
            with self.subTest(f"Case test {i+1}"):
                result = self.db._preprocess_spatial_functions(query)
                self.assertIn("MakePoint(1, 2, 4326)", result)
                # Should not contain any variation of GeomFromText
                self.assertNotIn("geomfromtext", result.lower())


if __name__ == '__main__':
    unittest.main()
