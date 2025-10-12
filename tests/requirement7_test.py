import pytest
from library_service import (
    get_patron_status_report
)

def test_patron_with_no_borrowed_books():
    """patron with no borrowed books"""
    result = get_patron_status_report("123457")

    assert isinstance(result,dict)
    assert result["currently borrowed"] == []
    assert result["fee amount"] == 0.00
    assert isinstance(result["borrowing history"], list)

def test_patron_with_one_book_borrowed_no_late_fees():
    """patron with one book borrowed and no late fees"""
    result = get_patron_status_report("123458")

    assert "currently borrowed" in result
    assert len(result["currently borrowed"]) == 1
    assert result["num borrowed books"] == 1
    assert "due date" in result["currently borrowed"][0]

def test_patron_with_muliple_books_and_late_fees():
    """patron with multiple books borrowed and late fees in their report"""
    result = get_patron_status_report("123459")

    assert result["num borrowed books"] == len(result["currently borrowed"])
    assert result["fee amount"] >= 0.00

def test_patron_with_borrowing_history():
    """patron with a hisotry of borrowed books"""
    result = get_patron_status_report("123450")

    assert "borrowing history" in result
    assert isinstance(result["borrowing history"],list)
    if result["borrowing history"]:
        assert "book id" in result["borrowing history"][0]

def test_invalid_patron_id():
    """Invalid patron id"""
    result = get_patron_status_report("invalid_patron")

    assert result["currently borrowed"] == []
    assert result["fee amount"] == 0.00
    assert result["num borrowed books"] == 0
    assert result["borrowing_history"] == []

#new tests after implementation
def test_valid_patron_id_returns_dictionary():
    """a patron with a valid id will alwways return a dictionary of their status report"""
    result = get_patron_status_report("123456")
    
    assert(result, dict)
    assert "total_borrowed" in result
    assert "total_late_fees" in result
    assert "borrowed_books" in result