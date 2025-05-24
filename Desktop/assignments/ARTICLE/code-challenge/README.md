# Code Challenge: SQL Database Project

This project is designed to demonstrate the use of a SQL database with Python. It includes models for authors, articles, and magazines, along with database connection setup, seeding functionality, and testing.

## Project Structure

```
code-challenge/
├── lib/ # Main code directory
│   ├── models/ # Model classes for database entities
│   ├── db/ # Database components including connection and schema
│   ├── controllers/ # Optional: Business logic
│   ├── debug.py # Interactive debugging
│   └── __init__.py # Makes lib a package
├── tests/ # Test directory for unit tests
├── scripts/ # Helper scripts for database setup and query execution
└── README.md # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.x
- A SQL database (e.g., SQLite, PostgreSQL, MySQL)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd code-challenge
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### Database Setup

To set up the database, run the following script:
```
python scripts/setup_db.py
```

This script will create the necessary tables and seed the database with initial data.

### Running Queries

To run example queries against the database, use:
```
python scripts/run_queries.py
```

### Running Tests

To ensure that all components are functioning correctly, run the tests:
```
pytest tests/
```

## Usage

- The `lib/models` directory contains classes for managing authors, articles, and magazines, each with SQL methods for CRUD operations.
- The `lib/db` directory handles database connections and schema definitions.
- The `lib/controllers` directory can be used to implement business logic if needed.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.