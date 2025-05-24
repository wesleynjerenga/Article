import unittest
from lib.models.magazine import Magazine

class TestMagazine(unittest.TestCase):

    def setUp(self):
        self.magazine = Magazine()

    def test_create_magazine(self):
        result = self.magazine.create("Test Magazine", "2023-01-01")
        self.assertTrue(result)

    def test_get_magazine(self):
        self.magazine.create("Test Magazine", "2023-01-01")
        result = self.magazine.get("Test Magazine")
        self.assertEqual(result['title'], "Test Magazine")

    def test_update_magazine(self):
        self.magazine.create("Test Magazine", "2023-01-01")
        result = self.magazine.update("Test Magazine", {"title": "Updated Magazine"})
        self.assertTrue(result)
        updated_result = self.magazine.get("Updated Magazine")
        self.assertEqual(updated_result['title'], "Updated Magazine")

    def test_delete_magazine(self):
        self.magazine.create("Test Magazine", "2023-01-01")
        result = self.magazine.delete("Test Magazine")
        self.assertTrue(result)
        deleted_result = self.magazine.get("Test Magazine")
        self.assertIsNone(deleted_result)

if __name__ == '__main__':
    unittest.main()