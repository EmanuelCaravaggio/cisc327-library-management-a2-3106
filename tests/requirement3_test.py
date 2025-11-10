import pytest
from unittest.mock import Mock, patch
from services.library_service import (
    borrow_book_by_patron,add_book_to_catalog
)


def test_borrow_book_valid_input(mocker):
    # Mock book lookup
    mocker.patch("services.library_service.get_book_by_id",
                 return_value={"id": 83, "title": "Some Book", "author": "Author",
                               "isbn": "1234567890123", "total_copies": 5, "available_copies": 5})
    
    # Mock patron borrow count (currently has 0 books)
    mocker.patch("services.library_service.get_patron_borrow_count", return_value=0)
    
    # Mock inserting borrow record → succeed
    mocker.patch("services.library_service.insert_borrow_record", return_value=True)
    
    # Mock updating book availability → succeed
    mocker.patch("services.library_service.update_book_availability", return_value=True)

    success, message = borrow_book_by_patron("123456", 83)

    assert success is True
    assert "successfully borrowed" in message.lower()


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
    assert "book not found" in message.lower()


def test_borrow_book_invalid_ISBN_does_not_exist():
    """borrowing a book in the system where the book does not exist"""
    success, message = borrow_book_by_patron("123456",10)

    assert success == False
    assert "book not found" in message.lower()


# small additioanl tests to push coverage over 80%+
def test_borrow_invalid_patron_id():
    success, message = borrow_book_by_patron("abc", 1)
    assert not success
    assert "Invalid patron ID" in message

@patch("services.library_service.get_book_by_id", return_value=None)
def test_borrow_book_not_found(mock_get):
    success, message = borrow_book_by_patron("123456", 1)
    assert not success
    assert "Book not found" in message

@patch("services.library_service.get_book_by_id", return_value={"id": 1, "title": "Pride and Prejudice", "available_copies": 0})
def test_borrow_book_unavailable(mock_get):
    success, message = borrow_book_by_patron("123456", 1)
    assert not success
    assert "not available" in message