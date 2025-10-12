import pytest
from library_service import (
    return_book_by_patron
)

def test_return_valid_book_return_no_fees():
    """returning book with no fees calculated"""
    success, message = return_book_by_patron("123456",6)

    assert success == True
    assert "successfully returned" in message.lower()
    assert "late fee" not in message.lower()

def test_return_valid_book_return_late_fees():
    """returing book with late fees calculated"""
    success, message = return_book_by_patron("123456",2)

    assert success == True
    assert "late fee" in message.lower()
    assert any(char.isdigit() for char in message)


def test_return_invalid_book_not_borrowed():
    """trying to return a book that has not been borrowed"""
    success, message = return_book_by_patron("123456",5)

    assert success == False
    assert "not borrowed" in message.lower()

def test_return_invalid_book_nonexistent():
    """trying to return a book that is not in the catalog"""
    success, message = return_book_by_patron("12345",10)

    assert success == False
    assert "not found" in message

def test_return_book_already_returned():
    """trying to return a book that you have already returned"""
    success1, message1 = return_book_by_patron("1234567",6)

    assert success1 == True
    assert "successfully returned" in message1.lower()

    success2, message2 = return_book_by_patron("1234567",6)
    assert success2 == False
    assert "already returned" in message2.lower()

#new tests after implementation
def test_return_invalid_patron_id():
    """invalid patron id"""
    success, message = return_book_by_patron("abc123",1)
    assert success is False
    assert "invalid patron id" in message.lower()


