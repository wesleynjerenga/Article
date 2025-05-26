import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from lib.db.connection import get_connection

def seed_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    
    # Seed authors
    authors = [
        ("John Smith",),
        ("Jane Doe",),
        ("Bob Johnson",),
        ("Alice Williams",)
    ]
    
    cursor.executemany("INSERT INTO authors (name) VALUES (?)", authors)
    
    # Seed magazines
    magazines = [
        ("Tech Today", "Technology"),
        ("Science Weekly", "Science"),
        ("Business Review", "Business"),
        ("Health Monthly", "Health")
    ]
    
    cursor.executemany("INSERT INTO magazines (name, category) VALUES (?, ?)", magazines)
    
    # Get author and magazine IDs
    cursor.execute("SELECT id FROM authors")
    author_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM magazines")
    magazine_ids = [row[0] for row in cursor.fetchall()]
    
    # Seed articles
    articles = [
        ("The Future of AI", author_ids[0], magazine_ids[0]),
        ("Quantum Computing Explained", author_ids[0], magazine_ids[1]),
        ("Market Trends 2023", author_ids[1], magazine_ids[2]),
        ("Sustainable Business Practices", author_ids[1], magazine_ids[2]),
        ("Health Benefits of Meditation", author_ids[2], magazine_ids[3]),
        ("New Cancer Research", author_ids[3], magazine_ids[1]),
        ("Tech Startups to Watch", author_ids[0], magazine_ids[0]),
        ("The Impact of Remote Work", author_ids[1], magazine_ids[2]),
        ("Advances in Biotechnology", author_ids[2], magazine_ids[1]),
        ("Data Privacy Concerns", author_ids[3], magazine_ids[0])
    ]
    
    cursor.executemany("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", articles)
    
    conn.commit()
    conn.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()