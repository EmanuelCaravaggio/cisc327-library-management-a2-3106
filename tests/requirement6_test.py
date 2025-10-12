import pytest
from library_service import search_books_in_catalog

def test_search_partial_title_case_sensitive():
    result = search_books_in_catalog("Pride", "title")
    assert isinstance(result, list)
    assert any("Pride and Prejudice" in book["title"] for book in result)

def test_search_partial_author_case_insensitive():
    result = search_books_in_catalog("austen", "author")
    assert isinstance(result, list)
    assert any("Jane Austen" in book["author"] for book in result)

def test_search_exact_isbn():
    result = search_books_in_catalog("1234567890123", "isbn")
    assert isinstance(result, list)
    assert result[0]["isbn"] == "1234567890123"

def test_search_with_no_result_title():
    result = search_books_in_catalog("non existent book", "title")
    assert result == []

def test_search_with_no_result_isbn_incorrect():
    result = search_books_in_catalog("12345678901234", "isbn")
    assert result == []

def test_search_with_whitespace():
    result = search_books_in_catalog("    prid    ", "title")
    assert any("Pride and Prejudice" in book["title"] for book in result)
