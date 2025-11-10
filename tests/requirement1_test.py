import pytest
from services.library_service import (
    add_book_to_catalog
)



def test_add_book_valid_ipnut():
    """Adding a book to system with valid input"""
    success, message = add_book_to_catalog("Test book 3","test author 3","1234567890128", 9)

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


# small additioanl tests to push coverage over 80%+
def test_add_book_empty_title():
    success, message = add_book_to_catalog("", "Jane Austen", "1234567890123", 1)
    assert success is False
    assert "Title is required" in message

def test_add_book_long_title():
    long_title = "A" * 201
    success, message = add_book_to_catalog(long_title, "Jane Austen", "1234567890123", 1)
    assert success is False
    assert "Title must be less than 200" in message

def test_add_book_empty_author():
    success, message = add_book_to_catalog("Pride and Prejudice", "", "1234567890123", 1)
    assert success is False
    assert "Author is required" in message

def test_add_book_long_author():
    long_author = "A" * 101
    success, message = add_book_to_catalog("Pride and Prejudice", long_author, "1234567890123", 1)
    assert success is False
    assert "Author must be less than 100" in message