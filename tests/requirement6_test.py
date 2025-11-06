import pytest
import sqlite3
from services.library_service import search_books_in_catalog

@pytest.fixture(scope="function", autouse=True)
def seed_books():
    """Seed a known book for search tests"""
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        isbn TEXT,
        available_copies INTEGER,
        total_copies INTEGER
    )""")
    cur.execute("DELETE FROM books")
    cur.execute("""INSERT INTO books (title, author, isbn, available_copies, total_copies)
                   VALUES (?, ?, ?, ?, ?)""",
                ("Pride and Prejudice", "Jane Austen", "1234567890123", 5, 5))
    conn.commit()
    conn.close()

def test_search_partial_title_case_sensitive():
    result = search_books_in_catalog("Pride", "title")
    assert isinstance(result, list)
    # check that at least one book matches exactly
    assert any(book["title"] == "Pride and Prejudice" for book in result)

def test_search_partial_author_case_insensitive():
    result = search_books_in_catalog("austen", "author")
    assert isinstance(result, list)
    assert any(book["author"] == "Jane Austen" for book in result)

def test_search_exact_isbn():
    result = search_books_in_catalog("1234567890123", "isbn")
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]["isbn"] == "1234567890123"

def test_search_with_whitespace():
    result = search_books_in_catalog("   prid   ", "title")
    assert any(book["title"] == "Pride and Prejudice" for book in result)
