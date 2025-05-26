from lib.db.connection import get_connection
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def add_author_with_articles(author_name, articles_data):
    """
    Add an author and their articles in a single transaction
    articles_data: list of dicts with 'title' and 'magazine_id' keys
    """
    conn = get_connection()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # Insert author
        cursor.execute(
            "INSERT INTO authors (name) VALUES (?) RETURNING id",
            (author_name,)
        )
        result = cursor.fetchone()
        author_id = result[0] if result else None
        
        if not author_id:
            raise Exception("Failed to create author")
        
        # Insert articles
        for article in articles_data:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (article['title'], author_id, article['magazine_id'])
            )
        
        conn.execute("COMMIT")
        return Author.find_by_id(author_id)
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Transaction failed: {e}")
        return None
    finally:
        conn.close()

def update_magazine_with_articles(magazine_id, new_category, article_titles):
    """
    Update a magazine's category and add new articles in a single transaction
    article_titles: list of article titles to create (all by the same author)
    """
    conn = get_connection()
    try:
        conn.execute("BEGIN TRANSACTION")
        cursor = conn.cursor()
        
        # Update magazine category
        cursor.execute(
            "UPDATE magazines SET category = ? WHERE id = ?",
            (new_category, magazine_id)
        )
        
        if cursor.rowcount == 0:
            raise Exception(f"Magazine with ID {magazine_id} not found")
        
        # Get an author for the new articles
        cursor.execute("SELECT id FROM authors LIMIT 1")
        author_row = cursor.fetchone()
        if not author_row:
            raise Exception("No authors found in the database")
        
        author_id = author_row[0]
        
        # Create new articles
        for title in article_titles:
            cursor.execute(
                "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                (title, author_id, magazine_id)
            )
        
        conn.execute("COMMIT")
        return Magazine.find_by_id(magazine_id)
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Transaction failed: {e}")
        return None
    finally:
        conn.close()