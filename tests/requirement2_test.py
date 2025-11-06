import pytest
from services.library_service import (
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