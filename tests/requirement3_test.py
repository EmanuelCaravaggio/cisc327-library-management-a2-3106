import pytest
from library_service import (
    borrow_book_by_patron,add_book_to_catalog
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



def test_borrow_book_valid_input():
    """borrowing a book in the system successfully"""
    add_book_to_catalog("Pride and Prejudice","Jane Austen","1234567890123", 1)
    success, message = borrow_book_by_patron("123456", 1)
    assert success == True


def test_borrow_book_invalid_ID_too_short():
    """borrowing a book in the system where ID input is too short"""
    success, message = borrow_book_by_patron("12345",1)

    assert success == False
    assert "6 digits" in message

def test_borrow_book_invalid_ID_too_long():
    """borrowing a book in the system where ID input is too long"""
    success, message = borrow_book_by_patron("1234567",1)

    assert success == False
    assert "6 digits" in message

def test_borrow_book_invalid_book_unavailable():
    """borrowing a book in the system where the book is not available"""
    success, message = borrow_book_by_patron("123456",3)

    assert success == False
    assert "not available" in message.lower()


def test_borrow_book_invalid_ISBN_does_not_exist():
    """borrowing a book in the system where the book does not exist"""
    success, message = borrow_book_by_patron("123456",10)

    assert success == False
    assert "book not found" in message.lower()



