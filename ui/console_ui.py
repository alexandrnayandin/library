from bll.book_service import BookService
from bll.loan_service import LoanService
from bll.reader_service import ReaderService


class ConsoleUI:
    def __init__(self):
        self.book_service = BookService()
        self.reader_service = ReaderService()
        self.loan_service = LoanService()

    def run(self):
        while True:
            print("\n=== Система управления библиотекой ===")
            print("1. Добавить книгу")
            print("2. Показать все книги")
            print("3. Добавить читателя")
            print("4. Показать всех читателей")
            print("5. Оформить выдачу книги")
            print("6. Показать все выдачи")
            print("7. Оформить возврат книги")
            print("0. Выход")

            choice = input("Выберите действие: ").strip()

            try:
                if choice == "1":
                    self._add_book()
                elif choice == "2":
                    self._show_books()
                elif choice == "3":
                    self._add_reader()
                elif choice == "4":
                    self._show_readers()
                elif choice == "5":
                    self._issue_book()
                elif choice == "6":
                    self._show_loans()
                elif choice == "7":
                    self._return_book()
                elif choice == "0":
                    print("Выход из программы.")
                    break
                else:
                    print("Неверный выбор. Повторите ввод.")
            except ValueError as exc:
                print(f"Ошибка: {exc}")
            except Exception as exc:
                print(f"Непредвиденная ошибка: {exc}")

    def _add_book(self):
        print("\n--- Добавление книги ---")
        title = input("Название: ").strip()
        author_name = input("Автор: ").strip()
        genre_name = input("Жанр: ").strip()
        publisher_name = input("Издательство: ").strip()

        publish_year_text = input("Год издания (можно оставить пустым): ").strip()
        publish_year = int(publish_year_text) if publish_year_text else None

        isbn = input("ISBN (можно оставить пустым): ").strip() or None
        copies_available = int(input("Количество экземпляров: ").strip())

        book_id = self.book_service.add_book(
            title=title,
            author_name=author_name,
            genre_name=genre_name,
            publisher_name=publisher_name,
            publish_year=publish_year,
            isbn=isbn,
            copies_available=copies_available,
        )
        print(f"Книга успешно добавлена. ID = {book_id}")

    def _show_books(self):
        print("\n--- Список книг ---")
        books = self.book_service.get_all_books()
        if not books:
            print("Книг пока нет.")
            return

        for book in books:
            print(
                f"ID: {book['BookID']}, "
                f"Название: {book['Title']}, "
                f"Автор(ы): {book['Authors'] or 'не указан'}, "
                f"Жанр: {book['GenreName']}, "
                f"Издательство: {book['PublisherName']}, "
                f"Год: {book['PublishYear']}, "
                f"Доступно: {book['CopiesAvailable']}"
            )

    def _add_reader(self):
        print("\n--- Добавление читателя ---")
        full_name = input("ФИО: ").strip()
        phone = input("Телефон (можно оставить пустым): ").strip() or None
        email = input("Email (можно оставить пустым): ").strip() or None
        address = input("Адрес (можно оставить пустым): ").strip() or None

        reader_id = self.reader_service.add_reader(
            full_name=full_name,
            phone=phone,
            email=email,
            address=address,
        )
        print(f"Читатель успешно добавлен. ID = {reader_id}")

    def _show_readers(self):
        print("\n--- Список читателей ---")
        readers = self.reader_service.get_all_readers()
        if not readers:
            print("Читателей пока нет.")
            return

        for reader in readers:
            print(
                f"ID: {reader['ReaderID']}, "
                f"ФИО: {reader['FullName']}, "
                f"Телефон: {reader['Phone']}, "
                f"Email: {reader['Email']}, "
                f"Дата регистрации: {reader['RegistrationDate']}"
            )

    def _issue_book(self):
        print("\n--- Выдача книги ---")
        reader_id = int(input("Введите ID читателя: ").strip())
        book_id = int(input("Введите ID книги: ").strip())
        loan_id = self.loan_service.issue_book(reader_id=reader_id, book_id=book_id)
        print(f"Выдача оформлена. ID выдачи = {loan_id}")

    def _show_loans(self):
        print("\n--- Список выдач ---")
        loans = self.loan_service.get_all_loans()
        if not loans:
            print("Выдач пока нет.")
            return

        for loan in loans:
            print(
                f"ID: {loan['LoanID']}, "
                f"Читатель: {loan['ReaderName']}, "
                f"Книга: {loan['BookTitle']}, "
                f"Дата выдачи: {loan['IssueDate']}, "
                f"Вернуть до: {loan['DueDate']}, "
                f"Дата возврата: {loan['ReturnDate']}, "
                f"Статус: {loan['Status']}"
            )

    def _return_book(self):
        print("\n--- Возврат книги ---")
        loan_id = int(input("Введите ID выдачи: ").strip())
        self.loan_service.return_book(loan_id)
        print("Возврат оформлен.")
