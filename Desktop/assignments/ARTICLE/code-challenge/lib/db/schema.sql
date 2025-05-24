-- Drop existing tables if they exist
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS magazines;

-- Create authors table
CREATE TABLE authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Create magazines table
CREATE TABLE magazines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(255) NOT NULL
);

-- Create articles table with foreign key constraints
CREATE TABLE articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER NOT NULL,
    magazine_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
    FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_articles_author_id ON articles(author_id);
CREATE INDEX idx_articles_magazine_id ON articles(magazine_id);
CREATE INDEX idx_magazines_category ON magazines(category);
