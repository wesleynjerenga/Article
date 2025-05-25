import unittest
from lib.models.article import Article

class TestArticle(unittest.TestCase):

    def setUp(self):
        self.article = Article(title="Test Article", content="This is a test article.")

    def test_create_article(self):
        self.article.create()
        # Add assertions to verify the article was created in the database

    def test_read_article(self):
        self.article.create()
        fetched_article = Article.read(self.article.id)
        self.assertEqual(fetched_article.title, self.article.title)
        self.assertEqual(fetched_article.content, self.article.content)

    def test_update_article(self):
        self.article.create()
        self.article.title = "Updated Title"
        self.article.update()
        updated_article = Article.read(self.article.id)
        self.assertEqual(updated_article.title, "Updated Title")

    def test_delete_article(self):
        self.article.create()
        article_id = self.article.id
        self.article.delete()
        deleted_article = Article.read(article_id)
        self.assertIsNone(deleted_article)

if __name__ == '__main__':
    unittest.main()