from datetime import date

from dal.reader_repository import ReaderRepository


class ReaderService:
    def __init__(self):
        self.reader_repository = ReaderRepository()

    def add_reader(
        self,
        full_name: str,
        phone: str | None,
        email: str | None,
        address: str | None,
    ) -> int:
        if not full_name.strip():
            raise ValueError("ФИО читателя не может быть пустым.")

        registration_date = date.today().isoformat()
        return self.reader_repository.add_reader(
            full_name=full_name.strip(),
            phone=phone.strip() if phone else None,
            email=email.strip() if email else None,
            address=address.strip() if address else None,
            registration_date=registration_date,
        )

    def get_all_readers(self):
        return self.reader_repository.get_all_readers()
