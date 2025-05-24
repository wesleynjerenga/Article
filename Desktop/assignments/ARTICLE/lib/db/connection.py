import sqlite3
from contextlib import contextmanager
import os

@contextmanager
def get_connection():
    """Get a database connection with proper configuration."""
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize the database with schema."""
    with get_connection() as conn:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(current_dir, 'schema.sql')
        
        with open(schema_path) as f:
            conn.executescript(f.read())
        conn.commit() 