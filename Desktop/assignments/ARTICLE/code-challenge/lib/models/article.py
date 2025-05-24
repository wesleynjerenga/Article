from ..db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id
        self.id = id

    def save(self):
        """Save the article to the database."""
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute(
                    "UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                    (self.title, self.author_id, self.magazine_id, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                    (self.title, self.author_id, self.magazine_id)
                )
                self.id = cursor.lastrowid
            conn.commit()
        return self

    @classmethod
    def find_by_id(cls, id):
        """Find an article by ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
            article_data = cursor.fetchone()
            return cls(
                article_data['title'],
                article_data['author_id'],
                article_data['magazine_id'],
                article_data['id']
            ) if article_data else None

    @classmethod
    def find_by_title(cls, title):
        """Find an article by title."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
            article_data = cursor.fetchone()
            return cls(
                article_data['title'],
                article_data['author_id'],
                article_data['magazine_id'],
                article_data['id']
            ) if article_data else None

    def author(self):
        """Get the author of this article."""
        from .author import Author
        return Author.find_by_id(self.author_id)

    def magazine(self):
        """Get the magazine this article was published in."""
        from .magazine import Magazine
        return Magazine.find_by_id(self.magazine_id)

    @classmethod
    def find_by_author(cls, author_id):
        """Find all articles by a specific author."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM articles 
                WHERE author_id = ?
            """, (author_id,))
            return [cls(
                row['title'],
                row['author_id'],
                row['magazine_id'],
                row['id']
            ) for row in cursor.fetchall()]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        """Find all articles in a specific magazine."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM articles 
                WHERE magazine_id = ?
            """, (magazine_id,))
            return [cls(
                row['title'],
                row['author_id'],
                row['magazine_id'],
                row['id']
            ) for row in cursor.fetchall()]
