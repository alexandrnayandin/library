from dal.author_repository import AuthorRepository
from dal.book_repository import BookRepository
from dal.genre_repository import GenreRepository
from dal.publisher_repository import PublisherRepository


class BookService:
    def __init__(self):
        self.book_repository = BookRepository()
        self.author_repository = AuthorRepository()
        self.genre_repository = GenreRepository()
        self.publisher_repository = PublisherRepository()

    def add_book(
        self,
        title: str,
        author_name: str,
        genre_name: str,
        publisher_name: str,
        publish_year: int | None,
        isbn: str | None,
        copies_available: int,
    ) -> int:
        if not title.strip():
            raise ValueError("Название книги не может быть пустым.")
        if not author_name.strip():
            raise ValueError("Имя автора не может быть пустым.")
        if not genre_name.strip():
            raise ValueError("Жанр не может быть пустым.")
        if not publisher_name.strip():
            raise ValueError("Издательство не может быть пустым.")
        if copies_available < 1:
            raise ValueError("Количество экземпляров должно быть не меньше 1.")

        genre_id = self.genre_repository.get_or_create_genre(genre_name.strip())
        publisher_id = self.publisher_repository.get_or_create_publisher(publisher_name.strip())
        author_id = self.author_repository.get_or_create_author(author_name.strip())

        book_id = self.book_repository.add_book(
            title=title.strip(),
            isbn=isbn.strip() if isbn else None,
            publish_year=publish_year,
            copies_available=copies_available,
            genre_id=genre_id,
            publisher_id=publisher_id,
        )
        self.book_repository.link_author(book_id, author_id)
        return book_id

    def get_all_books(self):
        return self.book_repository.get_all_books()
