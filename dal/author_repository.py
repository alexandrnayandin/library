from dal.db import get_connection


class AuthorRepository:
    def get_or_create_author(self, full_name: str) -> int:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT AuthorID FROM Author WHERE FullName = ?", (full_name,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return row["AuthorID"]

        cursor.execute(
            "INSERT INTO Author (FullName, BirthDate, Country) VALUES (?, ?, ?)",
            (full_name, None, None)
        )
        author_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return author_id
