from lib.db.connection import get_connection

class Magazine:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazine (name) VALUES (?)", (name,))
        conn.commit()
        return cls(cursor.lastrowid, name)

    @classmethod
    def get(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazine WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return cls(row["id"], row["name"])
        return None