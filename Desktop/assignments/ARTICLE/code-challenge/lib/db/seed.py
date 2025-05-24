from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine

def seed_database():
    """Populate the database with test data."""
    # Create authors
    authors = [
        Author("John Smith").save(),
        Author("Jane Doe").save(),
        Author("Bob Johnson").save()
    ]

    # Create magazines
    magazines = [
        Magazine("Tech Weekly", "Technology").save(),
        Magazine("Science Today", "Science").save(),
        Magazine("Business Review", "Business").save()
    ]

    # Create articles
    articles = [
        Article("Python Programming Tips", authors[0].id, magazines[0].id).save(),
        Article("Machine Learning Basics", authors[0].id, magazines[0].id).save(),
        Article("Quantum Physics Explained", authors[1].id, magazines[1].id).save(),
        Article("Market Analysis 2024", authors[2].id, magazines[2].id).save(),
        Article("AI in Business", authors[0].id, magazines[2].id).save(),
        Article("Future of Computing", authors[1].id, magazines[0].id).save()
    ]

    return authors, magazines, articles

if __name__ == "__main__":
    from .connection import init_db
    init_db()
    seed_database()
else:
    from .connection import init_db
    init_db()
    seed_database()
