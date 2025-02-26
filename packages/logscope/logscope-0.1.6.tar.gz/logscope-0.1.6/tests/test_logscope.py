import os
import pytest
import sqlite3
from logscope.core import logger, query
from logscope.database import LogscopeDatabase
from logscope.tracing import trace, start_tracing, stop_tracing

# Constants
test_db_path = 'test_logscope.db'

@pytest.fixture(scope="module")
def cleanup_db():
    """Fixture to ensure the test database is cleaned up after tests."""
    yield
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

@pytest.fixture
def db_logger():
    """Fixture to provide a logger instance with a test database."""
    return logger(db_path=test_db_path, style='plain')

def test_logger_creation(db_logger, cleanup_db):
    """Test logger creation and log entry insertion."""
    db_logger("Test log entry 1")
    db_logger("Test log entry 2")

    # Check the database for inserted log entries
    result = query(db_path=test_db_path)
    assert len(result) == 2
    assert result[0]['message'] == "Test log entry 1"
    assert result[1]['message'] == "Test log entry 2"

def test_query_function(db_logger, cleanup_db):
    """Test querying the SQLite database."""
    db_logger("Log entry for query test")
    result = query("SELECT * FROM logs WHERE message = 'Log entry for query test'", db_path=test_db_path)
    assert len(result) == 1
    assert result[0]['message'] == "Log entry for query test"

def test_logscope_database_write_and_close(cleanup_db):
    """Test database write and close operations."""
    db = LogscopeDatabase(db_path=test_db_path)
    entry = {
        'timestamp': '2025-01-01 12:00:00.123456',
        'message': 'Database test log entry',
        'filename': 'test_file.py',
        'lineno': 42,
        'source': 'test_source',
        'function': 'test_function',
        'event_type': 'test_event'
    }
    db.write_log(entry)
    db.close()

    # Verify the entry in the database
    with sqlite3.connect(test_db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logs WHERE message = ?", (entry['message'],))
        result = cursor.fetchone()
        assert result is not None
        assert result['message'] == entry['message']

def test_tracing_decorator(cleanup_db):
    """Test the @trace decorator for function execution logging."""
    @trace(db_path=test_db_path)
    def traced_function(x, y):
        return x + y

    result = traced_function(3, 4)
    assert result == 7

    # Verify the trace logs in the database
    trace_logs = query("SELECT * FROM logs WHERE message LIKE 'Function call:%'", db_path=test_db_path)
    assert len(trace_logs) > 0
    assert any("traced_function" in log['message'] for log in trace_logs)

def test_tracing_start_and_stop(cleanup_db):
    """Test start_tracing and stop_tracing functions."""
    start_tracing(db_path=test_db_path)

    def test_function():
        return "test"

    test_function()
    stop_tracing()

    # Verify trace logs
    logs = query("SELECT * FROM logs WHERE message LIKE 'Function call:%'", db_path=test_db_path)
    assert len(logs) > 0
    assert any("test_function" in log['message'] for log in logs)

def test_logger_with_different_styles(cleanup_db):
    """Test logger with different styles (plain and colorful)."""
    plain_logger = logger(db_path=test_db_path, style='plain')
    plain_logger("Plain style log")

    colorful_logger = logger(db_path=test_db_path, style='colorful')
    colorful_logger("Colorful style log")

    # Verify logs in the database
    result = query(db_path=test_db_path)
    assert len(result) >= 2
    assert any("Plain style log" in log['message'] for log in result)
    assert any("Colorful style log" in log['message'] for log in result)

if __name__ == "__main__":
    pytest.main(["-v", __file__])
