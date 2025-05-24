import unittest
from lib.models.author import Author
from lib.db.connection import get_db_connection

class TestAuthor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.connection = get_db_connection()
        cls.author = Author(cls.connection)

    def test_create_author(self):
        author_id = self.author.create("John Doe", "john@example.com")
        self.assertIsNotNone(author_id)

    def test_read_author(self):
        author_id = self.author.create("Jane Doe", "jane@example.com")
        author = self.author.read(author_id)
        self.assertEqual(author['name'], "Jane Doe")
        self.assertEqual(author['email'], "jane@example.com")

    def test_update_author(self):
        author_id = self.author.create("Alice Smith", "alice@example.com")
        self.author.update(author_id, name="Alice Johnson", email="alice.johnson@example.com")
        author = self.author.read(author_id)
        self.assertEqual(author['name'], "Alice Johnson")
        self.assertEqual(author['email'], "alice.johnson@example.com")

    def test_delete_author(self):
        author_id = self.author.create("Bob Brown", "bob@example.com")
        self.author.delete(author_id)
        author = self.author.read(author_id)
        self.assertIsNone(author)

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

if __name__ == '__main__':
    unittest.main()