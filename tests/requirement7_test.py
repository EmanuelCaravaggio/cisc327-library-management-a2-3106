import pytest
from library_service import get_patron_status_report



def test_patron_with_no_borrowed_books():
    """patron with no borrowed books"""
    result = get_patron_status_report("123457")

    assert isinstance(result, dict)
    assert result["total_borrowed"] == 0
    assert result["total_late_fees"] == 0.0
    assert isinstance(result["borrowed_books"], list)
    assert result["currently_overdue"] == 0


def test_patron_with_one_book_borrowed_no_late_fees():
    """patron with one book borrowed and no late fees"""
    result = get_patron_status_report("123458")

    assert "borrowed_books" in result
    assert isinstance(result["borrowed_books"], list)
    assert "total_borrowed" in result
    assert isinstance(result["total_borrowed"], int)
    assert "total_late_fees" in result


def test_patron_with_multiple_books_and_late_fees():
    """patron with multiple books borrowed and late fees in their report"""
    result = get_patron_status_report("123459")

    assert isinstance(result, dict)
    assert "total_borrowed" in result
    assert "total_late_fees" in result
    assert result["total_late_fees"] >= 0.0


def test_patron_with_borrowing_history():
    """patron with a history of borrowed books"""
    result = get_patron_status_report("123450")

    assert "borrowed_books" in result
    assert isinstance(result["borrowed_books"], list)
    if result["borrowed_books"]:
        first_book = result["borrowed_books"][0]
        assert "book_id" in first_book or "title" in first_book


def test_invalid_patron_id():
    """Invalid patron id"""
    result = get_patron_status_report("invalid_patron")

    # For invalid IDs, function returns an error dictionary
    if "error" in result:
        assert "invalid patron id" in result["error"].lower()
    else:
        # If no error key, ensure default safe values
        assert result["total_borrowed"] == 0
        assert result["total_late_fees"] == 0.0
        assert result["currently_overdue"] == 0
        assert isinstance(result["borrowed_books"], list)


# new test after implementation
def test_valid_patron_id_returns_dictionary():
    """a patron with a valid id will always return a dictionary of their status report"""
    result = get_patron_status_report("123456")
    
    assert isinstance(result, dict)
    assert "total_borrowed" in result
    assert "total_late_fees" in result
    assert "borrowed_books" in result
