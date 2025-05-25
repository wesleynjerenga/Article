import unittest
from lib.models.author import Author

class TestAuthor(unittest.TestCase):

    def setUp(self):
        self.author = Author(name="Test Author", email="test@example.com")

    def test_create_author(self):
        self.author.create()
        self.assertIsNotNone(self.author.id)  # Assuming the create method assigns an ID

    def test_read_author(self):
        self.author.create()
        fetched_author = Author.read(self.author.id)
        self.assertEqual(fetched_author.name, self.author.name)
        self.assertEqual(fetched_author.email, self.author.email)

    def test_update_author(self):
        self.author.create()
        self.author.name = "Updated Author"
        self.author.update()
        updated_author = Author.read(self.author.id)
        self.assertEqual(updated_author.name, "Updated Author")

    def test_delete_author(self):
        self.author.create()
        author_id = self.author.id
        self.author.delete()
        deleted_author = Author.read(author_id)
        self.assertIsNone(deleted_author)  # Assuming read returns None if not found

if __name__ == '__main__':
    unittest.main()