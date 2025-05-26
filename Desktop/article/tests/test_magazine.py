import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection

class TestMagazine(unittest.TestCase):
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
        
        cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Another Author",))
        self.another_author_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Test Magazine", "Test Category"))
        self.test_magazine_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                       ("Test Article", self.test_author_id, self.test_magazine_id))
        self.test_article_id = cursor.lastrowid
        
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                       ("Another Article", self.another_author_id, self.test_magazine_id))
        self.another_article_id = cursor.lastrowid
        
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
        magazine = Magazine.find_by_id(self.test_magazine_id)
        self.assertIsNotNone(magazine)
        self.assertEqual(magazine.name, "Test Magazine")
        self.assertEqual(magazine.category, "Test Category")
    
    def test_find_by_name(self):
        magazine = Magazine.find_by_name("Test Magazine")
        self.assertIsNotNone(magazine)
        self.assertEqual(magazine.id, self.test_magazine_id)
    
    def test_find_by_category(self):
        magazines = Magazine.find_by_category("Test Category")
        self.assertEqual(len(magazines), 1)
        self.assertEqual(magazines[0].id, self.test_magazine_id)
    
    def test_create(self):
        new_magazine = Magazine.create("New Magazine", "New Category")
        self.assertIsNotNone(new_magazine.id)
        self.assertEqual(new_magazine.name, "New Magazine")
        self.assertEqual(new_magazine.category, "New Category")
        
        # Verify in database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (new_magazine.id,))
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row['name'], "New Magazine")
        self.assertEqual(row['category'], "New Category")
    
    def test_save(self):
        # Test update
        magazine = Magazine.find_by_id(self.test_magazine_id)
        magazine.name = "Updated Magazine"
        magazine.category = "Updated Category"
        magazine.save()
        
        # Verify in database
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.test_magazine_id,))
        row = cursor.fetchone()
        self.assertEqual(row['name'], "Updated Magazine")
        self.assertEqual(row['category'], "Updated Category")
    
    def test_all(self):
        magazines = Magazine.all()
        self.assertGreaterEqual(len(magazines), 1)
        self.assertTrue(any(m.id == self.test_magazine_id for m in magazines))
    
    def test_articles(self):
        magazine = Magazine.find_by_id(self.test_magazine_id)
        articles = magazine.articles()
        self.assertEqual(len(articles), 2)
        article_titles = [a.title for a in articles]
        self.assertIn("Test Article", article_titles)
        self.assertIn("Another Article", article_titles)
    
    def test_contributors(self):
        magazine = Magazine.find_by_id(self.test_magazine_id)
        contributors = magazine.contributors()
        self.assertEqual(len(contributors), 2)
        contributor_names = [a.name for a in contributors]
        self.assertIn("Test Author", contributor_names)
        self.assertIn("Another Author", contributor_names)
    
    def test_article_titles(self):
        magazine = Magazine.find_by_id(self.test_magazine_id)
        titles = magazine.article_titles()
        self.assertEqual(len(titles), 2)
        self.assertIn("Test Article", titles)
        self.assertIn("Another Article", titles)
    
    def test_magazines_with_multiple_authors(self):
        magazines = Magazine.magazines_with_multiple_authors()
        self.assertEqual(len(magazines), 1)
        self.assertEqual(magazines[0].id, self.test_magazine_id)
    
    def test_count_articles(self):
        result = Magazine.count_articles()
        self.assertEqual(len(result), 1)
        magazine, count = result[0]
        self.assertEqual(magazine.id, self.test_magazine_id)
        self.assertEqual(count, 2)
    
    def test_contributing_authors(self):
        # Add more articles to trigger the "more than 2" condition
        magazine = Magazine.find_by_id(self.test_magazine_id)
        cursor = self.conn.cursor()
        
        # Add a third article by the first author
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                      ("Third Article", self.test_author_id, self.test_magazine_id))
        self.conn.commit()
        
        # Now test
        authors = magazine.contributing_authors()
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0].id, self.test_author_id)
    
    def test_top_publisher(self):
        top_magazine = Magazine.top_publisher()
        self.assertIsNotNone(top_magazine)
        self.assertEqual(top_magazine.id, self.test_magazine_id)

if __name__ == '__main__':
    unittest.main()