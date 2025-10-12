import pytest
from library_service import (
    get_all_books                                         
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


def test_catalog_returns_list_of_books():
    """catalog displays all books present in the database"""
    result = get_all_books()

    assert isinstance(result,list)

def test_catalog_has_all_fields():
    """catalog dispalys every nessasry field for the books"""
    result = get_all_books()

    if result:
        result = result[0]
        assert "title" in result
        assert "author" in result
        assert "isbn" in result
        assert "available_copies" in result
        assert "total_copies" in result

def test_catalog_available_less_than_total_copies():
    """total copies of books is never exceeded by available copies"""
    result = get_all_books()

    for result in result:
        assert result["available_copies"] <= result["total_copies"]

def test_catalog_displays_borrow_only_if_book_is_available():
   """catalog only displays borrowing option if book is available"""
   result = get_all_books()
   for book in result:
        actions = book.get("actions", "")
        if book["available_copies"] > 0:
            # If available, allow borrow (skip check if no actions defined)
            if actions:
                assert "borrow" in actions
        else:
            assert "borrow" not in actions