from lib.db.connection import get_connection
import sqlite3

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, content, author_id, magazine_id):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO article (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)",
                    (title, content, author_id, magazine_id)
                )
                conn.commit()
                return cls(cursor.lastrowid, title, content, author_id, magazine_id)
        except sqlite3.Error as e:
            print(f"Error creating article: {e}")
            return None

    @classmethod
    def get(cls, id):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM article WHERE id = ?", (id,))
                row = cursor.fetchone()
                if row:
                    return cls(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"])
                return None
        except sqlite3.Error as e:
            print(f"Error fetching article: {e}")
            return None

    @classmethod
    def update(cls, id, title=None, content=None):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                if title:
                    cursor.execute("UPDATE article SET title = ? WHERE id = ?", (title, id))
                if content:
                    cursor.execute("UPDATE article SET content = ? WHERE id = ?", (content, id))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating article: {e}")

    @classmethod
    def delete(cls, id):
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM article WHERE id = ?", (id,))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting article: {e}")