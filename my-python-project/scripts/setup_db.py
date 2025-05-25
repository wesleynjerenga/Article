import sqlite3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from lib.db.connection import get_connection

def setup_database(db_path):
    # Create a database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Read the SQL schema from the schema.sql file
    with open(os.path.join(os.path.dirname(__file__), '../lib/db/schema.sql'), 'r') as f:
        schema = f.read()

    # Execute the schema to create tables
    cursor.executescript(schema)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def seed_database(db_path):
    # Import the seed function from the seed module
    from lib.db.seed import seed_data

    # Seed the database with initial data
    seed_data(db_path)

def setup():
    conn = get_connection()
    with open("lib/db/schema.sql") as f:
        conn.executescript(f.read())
    print("Database initialized.")

if __name__ == "__main__":
    setup()