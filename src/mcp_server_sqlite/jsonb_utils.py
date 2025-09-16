"""JSONB utilities for SQLite"""
import json
import sqlite3

def validate_json(json_str):
    """Validate JSON string"""
    try:
        json.loads(json_str)
        return True
    except (json.JSONDecodeError, TypeError):
        return False

def convert_to_jsonb(conn, json_str):
    """Convert JSON string to JSONB binary format"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT jsonb(?)", (json_str,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception:
        return None

def convert_from_jsonb(conn, jsonb_data):
    """Convert JSONB binary data back to JSON string"""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT json(?)", (jsonb_data,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception:
        return None