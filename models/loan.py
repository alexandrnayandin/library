from dataclasses import dataclass


@dataclass
class Loan:
    loan_id: int | None
    reader_id: int
    book_id: int
    librarian_id: int
    issue_date: str
    due_date: str
    return_date: str | None
    status: str
