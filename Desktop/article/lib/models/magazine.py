from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id
        self.name = name
        self.category = category
    
    def save(self):
        conn = get_connection()
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
        conn.close()
        return self
    
    @classmethod
    def create(cls, name, category):
        magazine = cls(name, category)
        return magazine.save()
    
    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return cls(row['name'], row['category'], row['id'])
        return None
    
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return cls(row['name'], row['category'], row['id'])
        return None
    
    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        
        conn.close()
        
        return [cls(row['name'], row['category'], row['id']) for row in rows]
    
    @classmethod
    def all(cls):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM magazines")
        rows = cursor.fetchall()
        
        conn.close()
        
        return [cls(row['name'], row['category'], row['id']) for row in rows]
    
    def articles(self):
        from lib.models.article import Article
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        
        articles_data = cursor.fetchall()
        conn.close()
        
        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in articles_data]
    
    def contributors(self):
        from lib.models.author import Author
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT au.* FROM authors au
            JOIN articles ar ON au.id = ar.author_id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        
        authors_data = cursor.fetchall()
        conn.close()
        
        return [Author(row['name'], row['id']) for row in authors_data]
    
    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT title FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        
        titles = [row['title'] for row in cursor.fetchall()]
        conn.close()
        
        return titles
    
    def contributing_authors(self):
        from lib.models.author import Author
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT au.*, COUNT(ar.id) as article_count
            FROM authors au
            JOIN articles ar ON au.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY au.id
            HAVING article_count >= 2
        """, (self.id,))
        
        authors_data = cursor.fetchall()
        conn.close()
        
        return [Author(row['name'], row['id']) for row in authors_data]
    
    @classmethod
    def magazines_with_multiple_authors(cls):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT m.* 
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            HAVING COUNT(DISTINCT a.author_id) >= 2
        """)
        
        magazines_data = cursor.fetchall()
        conn.close()
        
        return [cls(row['name'], row['category'], row['id']) for row in magazines_data]
    
    @classmethod
    def count_articles(cls):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT m.id, m.name, m.category, COUNT(a.id) as article_count
            FROM magazines m
            LEFT JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
        """)
        
        result = cursor.fetchall()
        conn.close()
        
        return [(cls(row['name'], row['category'], row['id']), row['article_count']) for row in result]
    
    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT m.*, COUNT(a.id) as article_count
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(row['name'], row['category'], row['id'])
        return None