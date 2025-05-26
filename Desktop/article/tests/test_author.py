import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.connection import get_connection

class TestAuthor(unittest.TestCase):
    def setUp(self):
        # Create a test database
        self.conn = get_connection()
        cursor = self.conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        
        # Create test data
        cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Test Author",))
        self.test_author_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Test Magazine", "Test Category"))
        self.test_magazine_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                       ("Test Article", self.test_author_id, self.test_magazine_id))
        self.test_article_id = cursor.lastrowid
        
        self.conn.commit()
    
    def tearDown(self):
        # Clean up test data
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM articles")
        cursor.execute("DELETE FROM authors")
        cursor.execute("DELETE FROM magazines")
        self.conn.commit()
        self.conn.close()
    
    def test_find_by_id(self):
        author = Author.find_by_id(self.test_author_id)
        self.assertIsNotNone(author)
        self.assertEqual(author.name, "Test Author")
    
    def test_find_by_name(self):
        author = Author.find_by_name("Test Author")
        self.assertIsNotNone(author)
        self.assertEqual(author.id, self.test_author_id)
    
    def test_create(self):
        new_author = Author.create("New Author")
        self.assertIsNotNone(new_author.id)
        self.assertEqual(new_author.name, "New Author")
        
        # Verify in database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (new_author.id,))
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row['name'], "New Author")
    
    def test_save(self):
        # Test update
        author = Author.find_by_id(self.test_author_id)
        author.name = "Updated Author"
        author.save()
        
        # Verify in database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.test_author_id,))
        row = cursor.fetchone()
        self.assertEqual(row['name'], "Updated Author")
    
    def test_all(self):
        authors = Author.all()
        self.assertGreaterEqual(len(authors), 1)
        self.assertTrue(any(a.id == self.test_author_id for a in authors))
    
    def test_articles(self):
        author = Author.find_by_id(self.test_author_id)
        articles = author.articles()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, "Test Article")
    
    def test_magazines(self):
        author = Author.find_by_id(self.test_author_id)
        magazines = author.magazines()
        self.assertEqual(len(magazines), 1)
        self.assertEqual(magazines[0].name, "Test Magazine")
    
    def test_add_article(self):
        author = Author.find_by_id(self.test_author_id)
        magazine = Magazine.find_by_id(self.test_magazine_id)
        
        new_article = author.add_article(magazine, "New Test Article")
        self.assertIsNotNone(new_article.id)
        
        # Verify in database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (new_article.id,))
        row = cursor.fetchone()
        self.assertEqual(row['title'], "New Test Article")
        self.assertEqual(row['author_id'], self.test_author_id)
        self.assertEqual(row['magazine_id'], self.test_magazine_id)
    
    def test_topic_areas(self):
        author = Author.find_by_id(self.test_author_id)
        topics = author.topic_areas()
        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0], "Test Category")

if __name__ == '__main__':
    unittest.main()