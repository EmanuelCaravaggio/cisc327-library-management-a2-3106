import pytest 
from services.library_service import calculate_late_fee_for_book, pay_late_fees, refund_late_fee_payment, add_book_to_catalog, borrow_book_by_patron, search_books_in_catalog
from services.payment_service import PaymentGateway
from database import get_book_by_id
import os
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

class UnixFS:
    @staticmethod
    def rm(filename):
        os.remove(filename)

def test_unix_fs(mocker):
    mocker.patch('os.remove')
    UnixFS.rm('file')
    os.remove.assert_called_once_with('file')

#STUBS 
def test_calculate_late_fee_for_book_stub(mocker):
    stub_borrowed_books = [
        {
            "book_id": 1,
            "borrow_date": datetime.now() - timedelta(days=10),
            "due_date": datetime.now() - timedelta(days=3)
        }
    ]
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=stub_borrowed_books)

    result = calculate_late_fee_for_book("123456", 1)
    assert result["fee_amount"] > 0
    assert result["days_overdue"] == 3

def test_get_book_by_id_stub(mocker):
    stub_book = {
        "id": 9,
        "title": "1984",
        "author": "George Orwell",
        "isbn": "8765943721234",
        "total_copies": 4,
        "available_copies": 4
    }

    mocker.patch("database.get_book_by_id", return_value=stub_book)

    from database import get_book_by_id  
    result = get_book_by_id(9)

    assert result["title"] == "1984"
    assert result["author"] == "George Orwell"


#MOCKS
# pay_late_fees tests
# Successful payment
def test_pay_late_fees_successful_payment_mock():
    with patch("services.library_service.calculate_late_fee_for_book") as mock_fee, \
         patch("services.library_service.get_book_by_id") as mock_book:

        mock_fee.return_value = {"fee_amount": 1.5, "days_overdue": 3}
        mock_book.return_value = {"id": 1, "title": "Test Book"}

        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.return_value = (True, "txn_123", "Payment successful")

        success, message, txn_id = pay_late_fees("123456", 1, payment_gateway=mock_gateway)

        mock_gateway.process_payment.assert_called_once_with(
            patron_id="123456",
            amount=1.5,
            description="Late fees for 'Test Book'"
        )

        assert success is True
        assert txn_id == "txn_123"
        assert "successful" in message.lower()


# Declined payment
def test_pay_late_fees_declined_payment_mock():
    with patch("services.library_service.calculate_late_fee_for_book") as mock_fee, \
         patch("services.library_service.get_book_by_id") as mock_book:

        mock_fee.return_value = {"fee_amount": 2.5, "days_overdue": 5}
        mock_book.return_value = {"id": 1, "title": "Test Book"}

        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.return_value = (False, None, "Payment declined")

        success, message, txn_id = pay_late_fees("123456", 1, payment_gateway=mock_gateway)

        mock_gateway.process_payment.assert_called_once_with(
            patron_id="123456",
            amount=2.5,
            description="Late fees for 'Test Book'"
        )

        assert success is False
        assert txn_id is None
        assert "declined" in message.lower()


# Invalid patron id
def test_pay_late_fees_invalid_id_mock():
    mock_gateway = Mock(spec=PaymentGateway)

    success, message, txn_id = pay_late_fees("123", 1, payment_gateway=mock_gateway)

    mock_gateway.process_payment.assert_not_called()
    assert success is False
    assert txn_id is None
    assert "invalid patron id" in message.lower()


# No late fees 
def test_pay_late_fees_zero_late_fees_mock():
    with patch("services.library_service.calculate_late_fee_for_book") as mock_fee, \
         patch("services.library_service.get_book_by_id") as mock_book:

        mock_fee.return_value = {"fee_amount": 0.0, "days_overdue": 0}
        mock_book.return_value = {"id": 1, "title": "Test Book"}

        mock_gateway = Mock(spec=PaymentGateway)
        success, message, txn_id = pay_late_fees("123456", 1, payment_gateway=mock_gateway)

        mock_gateway.process_payment.assert_not_called()
        assert success is False
        assert txn_id is None
        assert "no late fees" in message.lower()


# Network error 
def test_pay_late_fees_network_error_mock():
    with patch("services.library_service.calculate_late_fee_for_book") as mock_fee, \
         patch("services.library_service.get_book_by_id") as mock_book:

        mock_fee.return_value = {"fee_amount": 1.5, "days_overdue": 3}
        mock_book.return_value = {"id": 1, "title": "Test Book"}

        mock_gateway = Mock(spec=PaymentGateway)
        mock_gateway.process_payment.side_effect = ConnectionError("Network Error")

        success, message, txn_id = pay_late_fees("123456", 1, payment_gateway=mock_gateway)

        mock_gateway.process_payment.assert_called_once_with(
            patron_id="123456",
            amount=1.5,
            description="Late fees for 'Test Book'"
        )

        assert success is False
        assert txn_id is None
        assert "network error" in message.lower()



# refund_late_fee_payment tests

# Sucessfull refund
def test_refund_late_fee_successful_mock():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Refund Complete")

    success, message = refund_late_fee_payment("txn_123", 5.00, mock_gateway)

    mock_gateway.refund_payment.assert_called_once_with("txn_123", 5.00)
    assert success is True
    assert "Refund Complete" in message

# Invaid transaction id
def test_refund_late_fee_invalid_transaction_id_mock():
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment("123", 5.00, mock_gateway)

    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert "invalid transaction id" in message.lower()

# Invalid amount (too big)
def test_refund_late_fee_invalid_amount1_mock():
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment("txn_123", 20.00, mock_gateway)

    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert "exceeds maximum" in message.lower()

# # Invalid amount (zero)
def test_refund_late_fee_invalid_amount2_mock():
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment("txn_123", 0.00, mock_gateway)

    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert "greater than 0" in message.lower()

# Invalid amount (less than zero)
def test_refund_late_fee_invalid_amount3_mock():
    mock_gateway = Mock(spec=PaymentGateway)

    success, message = refund_late_fee_payment("txn_123", -1.00, mock_gateway)

    mock_gateway.refund_payment.assert_not_called()
    assert success is False
    assert "greater than 0" in message.lower()




# small additioanl tests to push coverage over 80%+
def test_process_payment_invalid_amount_zero():
    gateway = PaymentGateway()
    success, txn_id, message = gateway.process_payment("123456", 0)
    assert not success
    assert "Invalid amount" in message

def test_process_payment_amount_exceeds_limit():
    gateway = PaymentGateway()
    success, txn_id, message = gateway.process_payment("123456", 2000)
    assert not success
    assert "exceeds limit" in message

def test_process_payment_invalid_patron_id():
    gateway = PaymentGateway()
    success, txn_id, message = gateway.process_payment("12345", 50)
    assert not success
    assert "Invalid patron ID" in message

def test_process_payment_success():
    gateway = PaymentGateway()
    success, txn_id, message = gateway.process_payment("123456", 50)
    assert success
    assert txn_id.startswith("txn_")

def test_refund_payment_invalid_transaction_id():
    gateway = PaymentGateway()
    success, message = gateway.refund_payment("abc123", 10)
    assert not success
    assert "Invalid transaction ID" in message

def test_refund_payment_invalid_amount():
    gateway = PaymentGateway()
    success, message = gateway.refund_payment("txn_123456_1", 0)
    assert not success
    assert "Invalid refund amount" in message

def test_refund_payment_success():
    gateway = PaymentGateway()
    success, message = gateway.refund_payment("txn_123456_1", 50)
    assert success
    assert "Refund of $50.00" in message
