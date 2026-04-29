from dal.db import get_connection


class GenreRepository:
    def get_or_create_genre(self, genre_name: str) -> int:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT GenreID FROM Genre WHERE GenreName = ?", (genre_name,))
        row = cursor.fetchone()
        if row:
            conn.close()
            return row["GenreID"]

        cursor.execute(
            "INSERT INTO Genre (GenreName, Description) VALUES (?, ?)",
            (genre_name, None)
        )
        genre_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return genre_id
