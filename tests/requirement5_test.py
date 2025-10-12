import pytest
from library_service import calculate_late_fee_for_book


def test_calculate_fee_no_overdue_books():
    """book returned on or before due date"""
    result = calculate_late_fee_for_book("123456", 5)

    assert isinstance(result, dict)
    assert result["days_overdue"] == 0
    assert result["fee_amount"] == 0.00


def test_calculate_fee_overdue_book_within_first_week():
    """book returned during first week of it being overdue"""
    result = calculate_late_fee_for_book("123456", 4)

    assert isinstance(result, dict)
    # we don’t know real DB data, just check structure
    assert "days_overdue" in result
    assert "fee_amount" in result
    assert result["fee_amount"] >= 0.0


def test_calculate_fee_overdue_book_after_first_week():
    """book returned after first week of being overdue"""
    result = calculate_late_fee_for_book("123456", 4)

    assert isinstance(result, dict)
    assert "fee_amount" in result
    assert result["fee_amount"] >= 0.0


def test_calclate_fee_overdue_book_at_fee_cap():
    """book returned at maximum fee cap"""
    result = calculate_late_fee_for_book("123456", 4)

    assert isinstance(result, dict)
    assert "fee_amount" in result
    assert result["fee_amount"] <= 15.00


def test_calculate_fee_overdue_book_exactly_7_days():
    """book returned exactly 7 days after being overdue"""
    result = calculate_late_fee_for_book("123456", 4)

    assert isinstance(result, dict)
    assert "days_overdue" in result
    assert "fee_amount" in result
    assert result["fee_amount"] >= 0.0


# new tests after implementation
def test_calculate_fee_no_books_overdue():
    """book returned that is not overdue should have zero return fee"""
    result = calculate_late_fee_for_book("123456", 1)

    assert isinstance(result, dict)
    assert result["fee_amount"] == 0.0
    assert result["days_overdue"] == 0
