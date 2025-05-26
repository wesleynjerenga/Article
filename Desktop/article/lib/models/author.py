from lib.db.connection import get_connection

class Author:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name
    
    def save(self):
        conn = get_connection()
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
        conn.close()
        return self
    
    @classmethod
    def create(cls, name):
        author = cls(name)
        return author.save()
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return cls(row['name'], row['id'])
        return None
    
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return cls(row['name'], row['id'])
        return None
    
    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()
        
        conn.close()
        
        return [cls(row['name'], row['id']) for row in rows]
    
    def articles(self):
        from lib.models.article import Article
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM articles
            WHERE author_id = ?
        """, (self.id,))
        
        articles_data = cursor.fetchall()
        conn.close()
        
        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in articles_data]
    
    def magazines(self):
        from lib.models.magazine import Magazine
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        
        magazines_data = cursor.fetchall()
        conn.close()
        
        return [Magazine(row['name'], row['category'], row['id']) for row in magazines_data]
    
    def add_article(self, magazine, title):
        from lib.models.article import Article
        
        article = Article(title, self.id, magazine.id)
        article.save()
        return article
    
    def topic_areas(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        
        categories = [row['category'] for row in cursor.fetchall()]
        conn.close()
        
        return categories
    
    @classmethod
    def find_author_with_most_articles(cls):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT a.id, a.name, COUNT(ar.id) as article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            GROUP BY a.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(row['name'], row['id'])
        return None