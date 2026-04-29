from dal.db import get_connection


class PublisherRepository:
    def get_or_create_publisher(self, publisher_name: str) -> int:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT PublisherID FROM Publisher WHERE PublisherName = ?",
            (publisher_name,)
        )
        row = cursor.fetchone()
        if row:
            conn.close()
            return row["PublisherID"]

        cursor.execute(
            "INSERT INTO Publisher (PublisherName, City, Phone) VALUES (?, ?, ?)",
            (publisher_name, None, None)
        )
        publisher_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return publisher_id
