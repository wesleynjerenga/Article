import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database

def main():
    print("Welcome to the Article-Author-Magazine Debug Console!")
    print("The following classes are available for testing:")
    print("- Author")
    print("- Magazine")
    print("- Article")
    print("\nSeeding the database for testing...")
    seed_database()
    print("Database seeded successfully!")
    
    print("\nExample usage:")
    print("author = Author.find_by_id(1)")
    print("print(author.name)")
    print("articles = author.articles()")
    print("for article in articles: print(article.title)")
    
    # Keep the console open
    try:
        from IPython import embed
        embed()
    except ImportError:
        import code
        code.interact(local=dict(globals(), **locals()))

if __name__ == "__main__":
    main()