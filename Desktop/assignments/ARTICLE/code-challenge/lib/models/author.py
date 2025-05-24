from ..db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    def save(self):
        """Save the author to the database."""
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute(
                    "UPDATE authors SET name = ? WHERE id = ?",
                    (self.name, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO authors (name) VALUES (?)",
                    (self.name,)
                )
                self.id = cursor.lastrowid
            conn.commit()
        return self

    @classmethod
    def find_by_id(cls, id):
        """Find an author by ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
            author_data = cursor.fetchone()
            return cls(author_data['name'], author_data['id']) if author_data else None

    @classmethod
    def find_by_name(cls, name):
        """Find an author by name."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
            author_data = cursor.fetchone()
            return cls(author_data['name'], author_data['id']) if author_data else None

    def articles(self):
        """Get all articles written by this author."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM articles 
                WHERE author_id = ?
            """, (self.id,))
            return cursor.fetchall()

    def magazines(self):
        """Get all magazines this author has contributed to."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.* FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            return cursor.fetchall()

    def topic_areas(self):
        """Get unique categories of magazines this author has contributed to."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.category FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self.id,))
            return [row['category'] for row in cursor.fetchall()]

    def add_article(self, magazine, title):
        """Add a new article for this author in a magazine."""
        from .article import Article
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        return article.save()
