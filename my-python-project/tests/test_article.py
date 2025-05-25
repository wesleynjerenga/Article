import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Reset the database before each test
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        DELETE FROM article;
        DELETE FROM author;
        DELETE FROM magazine;
        DELETE FROM sqlite_sequence WHERE name IN ('author', 'magazine', 'article');
    """)
    conn.commit()
    yield
    conn.close()

def test_create_and_get_article():
    author = Author.create("Test Author")
    magazine = Magazine.create("Test Magazine")
    article = Article.create("Test Title", "Test Content", author.id, magazine.id)
    assert article is not None
    fetched = Article.get(article.id)
    assert fetched is not None
    assert fetched.title == "Test Title"
    assert fetched.content == "Test Content"
    assert fetched.author_id == author.id
    assert fetched.magazine_id == magazine.id

def test_update_article():
    author = Author.create("Author2")
    magazine = Magazine.create("Magazine2")
    article = Article.create("Old Title", "Old Content", author.id, magazine.id)
    Article.update(article.id, title="New Title", content="New Content")
    updated = Article.get(article.id)
    assert updated.title == "New Title"
    assert updated.content == "New Content"

def test_delete_article():
    author = Author.create("Author3")
    magazine = Magazine.create("Magazine3")
    article = Article.create("Title", "Content", author.id, magazine.id)
    Article.delete(article.id)
    assert Article.get(article.id) is None