import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

class TestArticle(unittest.TestCase):
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
        article = Article.find_by_id(self.test_article_id)
        self.assertIsNotNone(article)
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.author_id, self.test_author_id)
        self.assertEqual(article.magazine_id, self.test_magazine_id)
    
    def test_find_by_title(self):
        articles = Article.find_by_title("Test Article")
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].id, self.test_article_id)
    
    def test_find_by_author_id(self):
        articles = Article.find_by_author_id(self.test_author_id)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].id, self.test_article_id)
    
    def test_find_by_magazine_id(self):
        articles = Article.find_by_magazine_id(self.test_magazine_id)
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].id, self.test_article_id)
    
    def test_create(self):
        new_article = Article.create("New Article", self.test_author_id, self.test_magazine_id)
        self.assertIsNotNone(new_article.id)
        self.assertEqual(new_article.title, "New Article")
        
        # Verify in database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (new_article.id,))
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row['title'], "New Article")
        self.assertEqual(row['author_id'], self.test_author_id)
        self.assertEqual(row['magazine_id'], self.test_magazine_id)
    
    def test_save(self):
        # Test update
        article = Article.find_by_id(self.test_article_id)
        article.title = "Updated Article"
        article.save()
        
        # Verify in database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (self.test_article_id,))
        row = cursor.fetchone()
        self.assertEqual(row['title'], "Updated Article")
    
    def test_all(self):
        articles = Article.all()
        self.assertGreaterEqual(len(articles), 1)
        self.assertTrue(any(a.id == self.test_article_id for a in articles))
    
    def test_author(self):
        article = Article.find_by_id(self.test_article_id)
        author = article.author()
        self.assertIsNotNone(author)
        self.assertEqual(author.id, self.test_author_id)
        self.assertEqual(author.name, "Test Author")
    
    def test_magazine(self):
        article = Article.find_by_id(self.test_article_id)
        magazine = article.magazine()
        self.assertIsNotNone(magazine)
        self.assertEqual(magazine.id, self.test_magazine_id)
        self.assertEqual(magazine.name, "Test Magazine")
        self.assertEqual(magazine.category, "Test Category")

if __name__ == '__main__':
    unittest.main()