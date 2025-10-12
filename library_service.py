"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    get_patron_borrowed_books, update_borrow_record_return_date, 
    get_all_books
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'



def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    
    TODO: Implement R4 as per requirements
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and was actually borrowed
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    borrowed_book = get_patron_borrowed_books(patron_id)
    borrowed_book = next((x for x in borrowed_book if x["book_id"] == book_id), None)
    if not borrowed_book:
        return False, "Book was not Borrowed by Patron"

    #record return date
    update_success = update_borrow_record_return_date(patron_id,book_id,datetime.now())
    if not update_success:
        return False, "Database error occurred while updating patron borrow record"
    
    #update number of available copies
    if not update_book_availability(book_id, +1):
        return False, "Database error occurred while updating book availability."
    
    #calculate and return/display any late fees owed
    late_fees_owed = calculate_late_fee_for_book(patron_id,book_id)
    fee, overdue_days = late_fees_owed["fee_amount"], late_fees_owed["days_overdue"]

    if fee > 0:
        return True, (
            f'Successfully returned "{book["title"]}".'
            f'Overdue by {overdue_days} day(s). Late fee: ${fee:.2f}.'
        )
    else:
        return True, f'Successfully returned "{book["title"]}". No late fees owed.'
    



def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    
    borrowed_book = get_patron_borrowed_books(patron_id)
    record = next((b for b in borrowed_book if b["book_id"] == book_id), None)
    if not record:
        return {"fee_amount": 0.00, "days_overdue": 0}

    now = datetime.now()
    due_date = record["due_date"]
    days_overdue = (now - due_date).days

    if days_overdue <= 0:
        return {"fee_amount": 0.00, "days_overdue": 0}

    if days_overdue <= 7:
        fee = days_overdue * 0.5
    else:
        fee = 7 * 0.5 + (days_overdue - 7) * 1.0

    fee = min(fee, 15.0)

    return {"fee_amount": round(fee, 2), "days_overdue": days_overdue}

    

def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:

    if not search_term or not search_term.strip():
        return []

    search_term = search_term.strip().lower()
    results = []

    if search_type.lower() == "isbn":
        book = get_book_by_isbn(search_term)
        return [book] if book else []

    books = get_all_books()

    if search_type.lower() == "title":
        results = [b for b in books if search_term in b["title"].lower()]
    elif search_type.lower() == "author":
        results = [b for b in books if search_term in b["author"].lower()]

    return results

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    TODO: Implement R7 as per requirements
    """
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return {"error": "Invalid patron ID. Must be exactly 6 digits."}

    borrowed_books = get_patron_borrowed_books(patron_id)
    total_borrowed = len(borrowed_books)

    #total late fees
    total_late_fees = 0.0
    for b in borrowed_books:
        if b["is_overdue"]:
            fee_info = calculate_late_fee_for_book(patron_id, b["book_id"])
            total_late_fees += fee_info["fee_amount"]

    #patron status report
    report = {
        "patron_id": patron_id,
        "borrowed_books": borrowed_books,  
        "total_borrowed": total_borrowed,
        "total_late_fees": round(total_late_fees, 2),
        "currently_overdue": len([b for b in borrowed_books if b["is_overdue"]]),
    }

    return report
