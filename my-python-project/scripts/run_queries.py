import sqlite3

def run_queries():
    # Connect to the database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Example query: Fetch all authors
    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()
    print("Authors:")
    for author in authors:
        print(author)

    # Example query: Fetch all articles
    cursor.execute("SELECT * FROM articles")
    articles = cursor.fetchall()
    print("\nArticles:")
    for article in articles:
        print(article)

    # Example query: Fetch all magazines
    cursor.execute("SELECT * FROM magazines")
    magazines = cursor.fetchall()
    print("\nMagazines:")
    for magazine in magazines:
        print(magazine)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    run_queries()