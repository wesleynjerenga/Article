# Articles-Authors-Magazines SQL Relationship Model

This project models the relationship between Authors, Articles, and Magazines, with data persisted in a SQL database.

## Domain Relationships

- An `Author` can write many `Articles`
- A `Magazine` can publish many `Articles`
- An `Article` belongs to both an `Author` and a `Magazine`
- The `Author`-`Magazine` relationship is many-to-many

## Setup Instructions

### Option 1: Using Pipenv
1. Install dependencies
```
pipenv install pytest sqlite3
```
2. Activate the virtual environment
```
pipenv shell
```

### Option 2: Using venv
1. Create a virtual environment
```
python -m venv env
```
2. Activate virtual environment
```
# Mac/Linux
source env/bin/activate

# Windows
env\Scripts\activate
```
3. Install dependencies
```
pip install pytest
```

## Database Setup

This project uses SQLite for simplicity. The database connection is configured in `lib/db/connection.py`.

To set up the database:

```
python scripts/setup_db.py
```

To seed the database with test data:

```
python lib/db/seed.py
```

## Project Structure

```
project/
├── lib/                     # Main code directory
│   ├── models/              # Model classes
│   │   ├── __init__.py      # Makes models a package
│   │   ├── author.py        # Author class with SQL methods
│   │   ├── article.py       # Article class with SQL methods
│   │   └── magazine.py      # Magazine class with SQL methods
│   ├── db/                  # Database components
│   │   ├── __init__.py      # Makes db a package
│   │   ├── connection.py    # Database connection setup
│   │   ├── seed.py          # Seed data for testing
│   │   └── schema.sql       # SQL schema definitions
│   ├── controllers/         # Business logic
│   │   └── __init__.py      # Makes controllers a package
│   ├── debug.py             # Interactive debugging
│   └── __init__.py          # Makes lib a package
├── tests/                   # Test directory
│   ├── __init__.py          # Makes tests a package
│   ├── test_author.py       # Tests for Author class
│   ├── test_article.py      # Tests for Article class
│   └── test_magazine.py     # Tests for Magazine class
├── scripts/                 # Helper scripts
│   ├── setup_db.py          # Script to set up the database
│   └── run_queries.py       # Script to run example queries
└── README.md                # Project documentation
```

## Testing

Run tests with pytest:

```
pytest
```

## Interactive Debugging

For interactive debugging and exploration:

```
python lib/debug.py
```

This will open an interactive console with all model classes pre-imported.

## Example Queries

To see example queries in action:

```
python scripts/run_queries.py
```

This will demonstrate various relationships and SQL queries including:

1. Getting all articles by a specific author
2. Finding magazines an author has contributed to
3. Finding authors who have written for a specific magazine
4. Finding magazines with articles by multiple authors
5. Counting articles in each magazine
6. Finding the author who has written the most articles
7. And more...