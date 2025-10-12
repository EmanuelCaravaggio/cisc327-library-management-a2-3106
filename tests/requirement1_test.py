import pytest
from library_service import (
    add_book_to_catalog
)



def test_add_book_valid_ipnut():
    """Adding a book to system with valid input"""
    success, message = add_book_to_catalog("Test book 2","test author 2","1234567890127", 9)

    assert success == True
    assert "successfully added" in message.lower()


def test_add_book_invalid_isbn_too_short():
    """Adding a book to system with isbn too short"""
    success, message = add_book_to_catalog("Pride and Prejudice","Jane Austen","12345678", 4)

    assert success == False
    assert "13 digits" in message

def test_add_book_invalid_isbn_too_long():
    """Adding a book to system with isbn too long"""
    success, message = add_book_to_catalog("Pride and Prejudice","Jane Austen","123456789101112", 4)

    assert success == False
    assert "13 digits" in message

def test_add_book_invalid_copies_number_negative():
    """Adding a book to system with a non positive integer number of copies"""
    success, message = add_book_to_catalog("Pride and Prejudice","Jane Austen","1234567891011", -4)

    assert success == False
    assert "positive integer" in message

def test_add_book_invalid_book_title_too_long():
    """Adding a book to system with a book title too long"""
    success, message = add_book_to_catalog("A"*250,"Jane Austen","1234567891016", 4)

    assert success == False
    assert "title" in message.lower()

def test_add_book_invalid_author_name_too_long():
    """Adding a book to system with author name too long"""
    success, message = success, message = add_book_to_catalog("Pride and Prejudice","A"*150,"1234567891014", 4)

    assert success == False
    assert "author" in message.lower()
