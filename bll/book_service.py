from dataclasses import dataclass


@dataclass
class Book:
    book_id: int | None
    title: str
    isbn: str | None
    publish_year: int | None
    copies_available: int
    genre_name: str
    publisher_name: str
