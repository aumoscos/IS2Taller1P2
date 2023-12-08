from datetime import datetime, timedelta
from main import Library, Book

def test_validate_quantity_positive():
    library = Library()
    assert library.validate_quantity("3") == 3

def test_validate_quantity_negative():
    library = Library()
    assert library.validate_quantity("-3") == -1

def test_validate_quantity_invalid_input():
    library = Library()
    assert library.validate_quantity("abc") == -1

def test_calculate_due_date():
    library = Library()
    current_date = datetime.now()
    due_date = library.calculate_due_date()
    assert due_date == current_date + timedelta(days=14)

def test_calculate_late_fee():
    library = Library()
    current_date = datetime.now()
    due_date = current_date - timedelta(days=7)
    assert library.calculate_late_fee(due_date) == 7

def test_calculate_late_fee_no_late():
    library = Library()
    current_date = datetime.now()
    due_date = current_date + timedelta(days=7)
    assert library.calculate_late_fee(due_date) == 0

def test_checkout_books_success():
    library = Library()
    book = library.books[0]
    selections = [(book, 2)]
    result = library.checkout_books(selections)
    assert result is not -1

def test_checkout_books_not_enough_copies():
    library = Library()
    book = library.books[0]
    selections = [(book, book.quantity + 1)]
    result = library.checkout_books(selections)
    assert result == -1

def test_return_books_success():
    library = Library()
    book = library.books[0]
    book.checked_out = 2
    returned_books = [(book, 2)]
    library.return_books(returned_books)
    assert book.checked_out == 0

