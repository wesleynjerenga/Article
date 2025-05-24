from ..db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.name = name
        self.category = category
        self.id = id

    def save(self):
        """Save the magazine to the database."""
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self.name, self.category, self.id)
                )
            else:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            conn.commit()
        return self

    @classmethod
    def find_by_id(cls, id):
        """Find a magazine by ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
            magazine_data = cursor.fetchone()
            return cls(magazine_data['name'], magazine_data['category'], magazine_data['id']) if magazine_data else None

    @classmethod
    def find_by_name(cls, name):
        """Find a magazine by name."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
            magazine_data = cursor.fetchone()
            return cls(magazine_data['name'], magazine_data['category'], magazine_data['id']) if magazine_data else None

    def articles(self):
        """Get all articles published in this magazine."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM articles 
                WHERE magazine_id = ?
            """, (self.id,))
            return cursor.fetchall()

    def contributors(self):
        """Get all authors who have written for this magazine."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT a.* FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
            """, (self.id,))
            return cursor.fetchall()

    def article_titles(self):
        """Get all article titles in this magazine."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT title FROM articles 
                WHERE magazine_id = ?
            """, (self.id,))
            return [row['title'] for row in cursor.fetchall()]

    def contributing_authors(self):
        """Get authors with more than 2 articles in this magazine."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.*, COUNT(ar.id) as article_count
                FROM authors a
                JOIN articles ar ON a.id = ar.author_id
                WHERE ar.magazine_id = ?
                GROUP BY a.id
                HAVING article_count > 2
            """, (self.id,))
            return cursor.fetchall()

    @classmethod
    def top_publisher(cls):
        """Find the magazine with the most articles."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.*, COUNT(a.id) as article_count
                FROM magazines m
                LEFT JOIN articles a ON m.id = a.magazine_id
                GROUP BY m.id
                ORDER BY article_count DESC
                LIMIT 1
            """)
            magazine_data = cursor.fetchone()
            return cls(magazine_data['name'], magazine_data['category'], magazine_data['id']) if magazine_data else None
