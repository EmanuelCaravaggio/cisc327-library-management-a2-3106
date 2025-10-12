import pytest
from library_service import (
    search_books_in_catalog
)

import sqlite3
@pytest.fixture(scope="function", autouse=True)
def reset_db():
    """Reset DB before each test"""
    # Use context manager so connection always closes
    with sqlite3.connect("library.db") as conn:
        cur = conn.cursor()
        # Make sure tables exist before deleting
        cur.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, isbn TEXT, available_copies INTEGER, total_copies INTEGER)")
        cur.execute("CREATE TABLE IF NOT EXISTS patrons (id INTEGER PRIMARY KEY, name TEXT)")
        cur.execute("DELETE FROM books")
        cur.execute("DELETE FROM patrons")
        conn.commit()


def test_search_partial_title_case_sensitive():
    """search catalog by partial title case sensitive"""
    result = search_books_in_catalog("Pride", "title")

    assert isinstance(result,list)
    assert any("Pride and Prejudice" in book["title"] for book in result)


def test_search_partial_author_case_insensitive():
    """search catalog by partial author name case insensitive"""
    result = search_books_in_catalog("austen", "author")

    assert isinstance(result, list)
    assert any("Jane Austen" in book["author"] for book in result)

def test_search_exact_isbn():
    """search catalog by exact isbn"""
    result = search_books_in_catalog("1234567890123", "isbn")

    assert isinstance(result, list)
    assert result[0]["isbn"] == "1234567890123"

def test_search_with_no_result_title():
    """search catalog with book title that is not in catalog"""
    result = search_books_in_catalog("non existent book", "title")

    assert result == []

def test_search_with_no_result_isbn_incorrect():
    """search catalog with isbn that is invalid (too long)"""
    result = search_books_in_catalog("12345678901234", "isbn")

    assert result == []

#new tests after implementation
def test_search_with_whitespace():
    """search catalog with extra whitespace"""
    result = search_books_in_catalog("    prid    ", "title")
    assert any("Pride and Prejudice" in book["title"] for book in result)
    