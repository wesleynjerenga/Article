import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from lib.db.seed import seed_database
from lib.db.transaction import add_author_with_articles, update_magazine_with_articles

def print_divider():
    print("\n" + "-" * 50 + "\n")

def run_example_queries():
    print("Seeding the database with test data...")
    seed_database()
    print("Database seeded successfully!")
    
    print_divider()
    print("1. All authors in the database:")
    for author in Author.all():
        print(f"Author ID: {author.id}, Name: {author.name}")
    
    print_divider()
    print("2. All magazines in the database:")
    for magazine in Magazine.all():
        print(f"Magazine ID: {magazine.id}, Name: {magazine.name}, Category: {magazine.category}")
    
    print_divider()
    print("3. Articles for a specific author (Author ID: 1):")
    author = Author.find_by_id(1)
    if author:
        print(f"Articles by {author.name}:")
        for article in author.articles():
            print(f"- {article.title}")
    
    print_divider()
    print("4. Magazines a specific author has contributed to (Author ID: 1):")
    if author:
        print(f"Magazines {author.name} has written for:")
        for magazine in author.magazines():
            print(f"- {magazine.name} ({magazine.category})")
    
    print_divider()
    print("5. Authors who have written for a specific magazine (Magazine ID: 1):")
    magazine = Magazine.find_by_id(1)
    if magazine:
        print(f"Contributors to {magazine.name}:")
        for contributor in magazine.contributors():
            print(f"- {contributor.name}")
    
    print_divider()
    print("6. Magazines with articles by at least 2 different authors:")
    for magazine in Magazine.magazines_with_multiple_authors():
        print(f"- {magazine.name}")
    
    print_divider()
    print("7. Number of articles in each magazine:")
    for magazine, count in Magazine.count_articles():
        print(f"- {magazine.name}: {count} articles")
    
    print_divider()
    print("8. Author who has written the most articles:")
    top_author = Author.find_author_with_most_articles()
    if top_author:
        print(f"{top_author.name} has written the most articles")
        print(f"Articles: {len(top_author.articles())}")
    
    print_divider()
    print("9. Topic areas an author writes about (Author ID: 1):")
    if author:
        print(f"Topic areas for {author.name}:")
        for category in author.topic_areas():
            print(f"- {category}")
    
    print_divider()
    print("10. Magazine with the most articles (top publisher):")
    top_magazine = Magazine.top_publisher()
    if top_magazine:
        print(f"{top_magazine.name} is the top publisher")
        print(f"Articles: {len(top_magazine.articles())}")
    
    print_divider()
    print("11. Transaction example - adding an author with multiple articles:")
    magazine_ids = [m.id for m in Magazine.all()]
    if magazine_ids:
        articles_data = [
            {'title': 'Transaction Article 1', 'magazine_id': magazine_ids[0]},
            {'title': 'Transaction Article 2', 'magazine_id': magazine_ids[-1]}
        ]
        new_author = add_author_with_articles("Transaction Author", articles_data)
        if new_author:
            print(f"Created author: {new_author.name} (ID: {new_author.id})")
            print("Articles created:")
            for article in new_author.articles():
                print(f"- {article.title}")
    
    print_divider()
    print("12. Transaction example - updating a magazine with new articles:")
    magazines = Magazine.all()
    if magazines:
        updated_magazine = update_magazine_with_articles(
            magazines[0].id, 
            "Updated Category",
            ["New Transaction Article 1", "New Transaction Article 2"]
        )
        if updated_magazine:
            print(f"Updated magazine: {updated_magazine.name}")
            print(f"New category: {updated_magazine.category}")
            print("All articles in this magazine:")
            for article in updated_magazine.articles():
                print(f"- {article.title}")

if __name__ == "__main__":
    run_example_queries()