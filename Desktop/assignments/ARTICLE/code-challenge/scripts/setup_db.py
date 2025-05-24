import sqlite3
import os

def setup_database(db_file):
    if os.path.exists(db_file):
        os.remove(db_file)

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    with open(os.path.join(os.path.dirname(__file__), '../lib/db/schema.sql'), 'r') as f:
        cursor.executescript(f.read())

    connection.commit()
    connection.close()

def seed_database(db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    with open(os.path.join(os.path.dirname(__file__), '../lib/db/seed.py'), 'r') as f:
        exec(f.read())

    connection.commit()
    connection.close()

if __name__ == "__main__":
    db_file = 'database.db'
    setup_database(db_file)
    seed_database(db_file)
    print("Database setup and seeded successfully.")