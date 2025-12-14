from datetime import datetime, timedelta
from models.books import Book


class Library:
    def __init__(self):
        """
        borrowed_books:
        key   -> (user_name, book_id)
        value -> due_date
        """
        self.books = {}
        self.borrowed_books = {}

    # 1. Add Book
    def add_book(self, book_id, title, author, total):
        if book_id in self.books:
            return False
        self.books[book_id] = Book(book_id, title, author, total)
        return True

    # 2. Search Book by Title
    def search_by_title(self, title):
        result = []
        for book in self.books.values():
            if title.lower() in book.title.lower():
                result.append(book)
        return result

    # 3. Search Book by Author
    def search_by_author(self, author):
        result = []
        for book in self.books.values():
            if author.lower() in book.author.lower():
                result.append(book)
        return result

    # 4. Borrow Book
    def borrow_book(self, name, book_id):
        if book_id not in self.books:
            return None, "Invalid Book ID"

        book = self.books[book_id]
        if book.available_copies <= 0:
            return None, "Book Not Available"

        due_date = datetime.now() + timedelta(days=7)
        book.available_copies -= 1
        self.borrowed_books[(name, book_id)] = due_date
        return due_date, None

    # 5. Return Book
    def return_book(self, name, book_id):
        key = (name, book_id)
        if key not in self.borrowed_books:
            return None

        due_date = self.borrowed_books[key]
        fine = self.calculate_fine(due_date, datetime.now())
        self.books[book_id].available_copies += 1
        del self.borrowed_books[key]
        return fine

    # Fine calculation
    def calculate_fine(self, due_date, return_date):
        if return_date > due_date:
            days_late = (return_date - due_date).days
            return days_late * 10
        return 0

    # 6. View Borrowed Books
    def get_borrowed_books(self):
        return self.borrowed_books

    # 7. View All Books
    def get_all_books(self):
        return list(self.books.values())
