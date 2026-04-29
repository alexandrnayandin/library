from dal.db import get_connection


class LoanRepository:
    def create_loan(
        self,
        reader_id: int,
        book_id: int,
        librarian_id: int,
        issue_date: str,
        due_date: str,
        status: str,
    ) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Loan (ReaderID, BookID, LibrarianID, IssueDate, DueDate, ReturnDate, Status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (reader_id, book_id, librarian_id, issue_date, due_date, None, status),
        )
        loan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return loan_id

    def get_all_loans(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                l.LoanID,
                r.FullName AS ReaderName,
                b.Title AS BookTitle,
                l.IssueDate,
                l.DueDate,
                l.ReturnDate,
                l.Status
            FROM Loan l
            JOIN Reader r ON l.ReaderID = r.ReaderID
            JOIN Book b ON l.BookID = b.BookID
            ORDER BY l.LoanID
            """
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_active_loan_by_id(self, loan_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Loan WHERE LoanID = ? AND Status = 'Issued'",
            (loan_id,),
        )
        row = cursor.fetchone()
        conn.close()
        return row

    def return_loan(self, loan_id: int, return_date: str) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Loan
            SET ReturnDate = ?, Status = 'Returned'
            WHERE LoanID = ?
            """,
            (return_date, loan_id),
        )
        conn.commit()
        conn.close()
