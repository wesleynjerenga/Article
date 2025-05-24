import unittest
from lib.models.article import Article

class TestArticle(unittest.TestCase):

    def setUp(self):
        self.article = Article(title="Test Article", content="This is a test article.")

    def test_create_article(self):
        result = self.article.create()
        self.assertTrue(result)

    def test_read_article(self):
        self.article.create()
        result = self.article.read()
        self.assertEqual(result['title'], "Test Article")

    def test_update_article(self):
        self.article.create()
        self.article.title = "Updated Article"
        result = self.article.update()
        self.assertTrue(result)

    def test_delete_article(self):
        self.article.create()
        result = self.article.delete()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()