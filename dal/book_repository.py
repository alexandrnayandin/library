from dal.db import get_connection


class BookRepository:
    def add_book(
        self,
        title: str,
        isbn: str | None,
        publish_year: int | None,
        copies_available: int,
        genre_id: int,
        publisher_id: int,
    ) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Book (Title, ISBN, PublishYear, CopiesAvailable, GenreID, PublisherID)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, isbn, publish_year, copies_available, genre_id, publisher_id),
        )
        book_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return book_id

    def link_author(self, book_id: int, author_id: int) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO BookAuthor (BookID, AuthorID) VALUES (?, ?)",
            (book_id, author_id),
        )
        conn.commit()
        conn.close()

    def get_all_books(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                b.BookID,
                b.Title,
                b.ISBN,
                b.PublishYear,
                b.CopiesAvailable,
                g.GenreName,
                p.PublisherName,
                GROUP_CONCAT(a.FullName, ', ') AS Authors
            FROM Book b
            JOIN Genre g ON b.GenreID = g.GenreID
            JOIN Publisher p ON b.PublisherID = p.PublisherID
            LEFT JOIN BookAuthor ba ON b.BookID = ba.BookID
            LEFT JOIN Author a ON ba.AuthorID = a.AuthorID
            GROUP BY
                b.BookID, b.Title, b.ISBN, b.PublishYear,
                b.CopiesAvailable, g.GenreName, p.PublisherName
            ORDER BY b.BookID
            """
        )
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_book_by_id(self, book_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Book WHERE BookID = ?", (book_id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def decrease_available_copies(self, book_id: int) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Book
            SET CopiesAvailable = CopiesAvailable - 1
            WHERE BookID = ? AND CopiesAvailable > 0
            """,
            (book_id,),
        )
        conn.commit()
        conn.close()

    def increase_available_copies(self, book_id: int) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Book
            SET CopiesAvailable = CopiesAvailable + 1
            WHERE BookID = ?
            """,
            (book_id,),
        )
        conn.commit()
        conn.close()
