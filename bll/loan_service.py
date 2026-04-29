from datetime import date, timedelta

from dal.book_repository import BookRepository
from dal.loan_repository import LoanRepository
from dal.reader_repository import ReaderRepository


class LoanService:
    def __init__(self):
        self.loan_repository = LoanRepository()
        self.book_repository = BookRepository()
        self.reader_repository = ReaderRepository()

    def issue_book(self, reader_id: int, book_id: int, librarian_id: int = 1) -> int:
        reader = self.reader_repository.get_reader_by_id(reader_id)
        if reader is None:
            raise ValueError("Читатель с таким ID не найден.")

        book = self.book_repository.get_book_by_id(book_id)
        if book is None:
            raise ValueError("Книга с таким ID не найдена.")

        if book["CopiesAvailable"] <= 0:
            raise ValueError("Нет доступных экземпляров этой книги.")

        issue_date = date.today()
        due_date = issue_date + timedelta(days=14)

        loan_id = self.loan_repository.create_loan(
            reader_id=reader_id,
            book_id=book_id,
            librarian_id=librarian_id,
            issue_date=issue_date.isoformat(),
            due_date=due_date.isoformat(),
            status="Issued",
        )
        self.book_repository.decrease_available_copies(book_id)
        return loan_id

    def return_book(self, loan_id: int) -> None:
        loan = self.loan_repository.get_active_loan_by_id(loan_id)
        if loan is None:
            raise ValueError("Активная выдача с таким ID не найдена.")

        self.loan_repository.return_loan(loan_id, date.today().isoformat())
        self.book_repository.increase_available_copies(loan["BookID"])

    def get_all_loans(self):
        return self.loan_repository.get_all_loans()
