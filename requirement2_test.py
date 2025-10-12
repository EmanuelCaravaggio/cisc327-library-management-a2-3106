import pytest
from library_service import (
    get_all_books                                         
)

def test_catalog_returns_list_of_books():
    """catalog displays all books present in the database"""
    result = get_all_books()

    assert isinstance(result,list)

def test_catalog_has_all_fields():
    """catalog dispalys every nessasry field for the books"""
    result = get_all_books()

    if result:
        result = result[0]
        assert "book id" in result
        assert "title" in result
        assert "author" in result
        assert "isbn" in result
        assert "available copies" in result
        assert "total copies" in result

def test_catalog_available_less_than_total_copies():
    """total copies of books is never exceeded by available copies"""
    result = get_all_books()

    for result in result:
        assert result["available copies"] <= result["total copies"]

def test_catalog_displays_borrow_only_if_book_is_available():
    """catalog only displays borrowing option if book is available"""
    result = get_all_books()

    for result in result:
        if result["available copies"] > 0:
            assert "borrow" in result.get("actions","")
        else:
            assert "borrow" not in result.get("actions","")

def test_catalog_empty_if_nothing_is_in_catalog():
    """if catalog is empty nothing is dispalyed"""
    result = get_all_books()

    assert result == []

