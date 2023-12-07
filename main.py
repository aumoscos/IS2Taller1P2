
from datetime import datetime, timedelta


class Book:

  def __init__(self, title, author, quantity):
    self.title = title
    self.author = author
    self.quantity = quantity
    self.checked_out = 0


class Library:

  def __init__(self):
    self.books = [
        Book("Mistbron", "Brandon Sanderson", 5),
        Book("TLOTR", "J.R.R. Tolkien", 3),
        Book("Color out of Space", "H.P. Lovecraft", 7),
        # Add more books as needed
    ]

  def display_catalog(self):
    print("Catalog:")
    for book in self.books:
      print(f"{book.title} by {book.author} - Available: {book.quantity}")

  def validate_quantity(self, quantity_str):
    try:
      quantity = int(quantity_str)
      if quantity > 0:
        return quantity
      else:
        print("Invalid quantity. Please enter a positive integer.")
        return -1
    except ValueError:
      print("Invalid input. Please enter a valid number.")
      return -1

  def calculate_due_date(self):
    return datetime.now() + timedelta(days=14)

  def calculate_late_fee(self, due_date):
    today = datetime.now()
    if today > due_date:
      days_late = (today - due_date).days
      return days_late
    else:
      return 0

  def display_checkout_confirmation(self, selected_books):
    print("\nSelected Books:")
    total_late_fee = 0
    for book, quantity, due_date in selected_books:
      late_fee = self.calculate_late_fee(due_date)
      total_late_fee += late_fee
      print(
          f"{book.title} (Qty: {quantity}) - Due Date: {due_date.strftime('%Y-%m-%d')}, Late Fee: ${late_fee}"
      )

    print(f"\nTotal Late Fee: ${total_late_fee}")

  def checkout_books(self, selections):
    selected_books = []
    for selection in selections:
      book = selection[0]
      quantity = selection[1]

      if quantity <= book.quantity - book.checked_out:
        book.checked_out += quantity
        due_date = self.calculate_due_date()
        selected_books.append((book, quantity, due_date))
      else:
        print(
            f"Error: Not enough copies of {book.title} available for checkout."
        )
        return -1

    self.display_checkout_confirmation(selected_books)
    return selected_books

  def return_books(self, returned_books):
    total_late_fee = 0
    print("\nReturned Books:")
    for returned_book in returned_books:
      book, quantity = returned_book
      late_fee = self.calculate_late_fee(self.calculate_due_date())
      total_late_fee += late_fee
      book.checked_out -= quantity
      print(f"{book.title} (Qty: {quantity}) - Late Fee: ${late_fee}")

    print(f"\nTotal Late Fee: ${total_late_fee}")


def main():
  library = Library()

  while True:
    print("\n1. Display Catalog")
    print("2. Checkout Books")
    print("3. Return Books")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
      library.display_catalog()
    elif choice == "2":
      selections = []
      while True:
        library.display_catalog()
        title = input(
            "Enter the title of the book to checkout (or 'done' to finish): ")
        if title.lower() == 'done':
          break

        book = next(
            (b for b in library.books if b.title.lower() == title.lower()),
            None)
        if book:
          quantity_str = input(
              f"Enter the quantity of '{book.title}' to checkout: ")
          quantity = library.validate_quantity(quantity_str)
          if quantity != -1:
            selections.append((book, quantity))
        else:
          print("Error: Book not found in the catalog.")

      result = library.checkout_books(selections)
      if result != -1:
        print("Checkout successful!")
    elif choice == "3":
      returned_books = []
      while True:
        library.display_catalog()
        title = input(
            "Enter the title of the book to return (or 'done' to finish): ")
        if title.lower() == 'done':
          break

        book = next(
            (b for b in library.books if b.title.lower() == title.lower()),
            None)
        if book and book.checked_out > 0:
          quantity_str = input(
              f"Enter the quantity of '{book.title}' to return: ")
          quantity = library.validate_quantity(quantity_str)
          if quantity != -1 and quantity <= book.checked_out:
            returned_books.append((book, quantity))
          else:
            print(
                "Error: Invalid quantity or trying to return more than checked out."
            )
        elif book and book.checked_out == 0:
          print("Error: No copies of this book are currently checked out.")
        else:
          print("Error: Book not found in the catalog or not checked out.")

      library.return_books(returned_books)
    elif choice == "4":
      print("Exiting program. Goodbye!")
      break
    else:
      print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
  main()
