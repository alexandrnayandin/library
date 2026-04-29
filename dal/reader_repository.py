from dal.db import get_connection


class ReaderRepository:
    def add_reader(
        self,
        full_name: str,
        phone: str | None,
        email: str | None,
        address: str | None,
        registration_date: str,
    ) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO Reader (FullName, Phone, Email, Address, RegistrationDate)
            VALUES (?, ?, ?, ?, ?)
            """,
            (full_name, phone, email, address, registration_date),
        )
        reader_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return reader_id

    def get_all_readers(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reader ORDER BY ReaderID")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_reader_by_id(self, reader_id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reader WHERE ReaderID = ?", (reader_id,))
        row = cursor.fetchone()
        conn.close()
        return row
