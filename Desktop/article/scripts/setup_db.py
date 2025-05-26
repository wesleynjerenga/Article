import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.db.connection import get_connection

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    with open('lib/db/schema.sql', 'r') as schema_file:
        schema_sql = schema_file.read()
        cursor.executescript(schema_sql)
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()