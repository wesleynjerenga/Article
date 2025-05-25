import unittest
from lib.models.magazine import Magazine

class TestMagazine(unittest.TestCase):

    def setUp(self):
        self.magazine = Magazine(title="Test Magazine", publisher="Test Publisher")

    def test_create_magazine(self):
        self.assertEqual(self.magazine.title, "Test Magazine")
        self.assertEqual(self.magazine.publisher, "Test Publisher")

    def test_magazine_crud_operations(self):
        # Assuming the Magazine class has methods for CRUD operations
        self.magazine.create()
        retrieved_magazine = Magazine.read(self.magazine.id)
        self.assertEqual(retrieved_magazine.title, self.magazine.title)

        self.magazine.title = "Updated Magazine"
        self.magazine.update()
        updated_magazine = Magazine.read(self.magazine.id)
        self.assertEqual(updated_magazine.title, "Updated Magazine")

        self.magazine.delete()
        deleted_magazine = Magazine.read(self.magazine.id)
        self.assertIsNone(deleted_magazine)

if __name__ == '__main__':
    unittest.main()