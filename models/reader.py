from dataclasses import dataclass


@dataclass
class Reader:
    reader_id: int | None
    full_name: str
    phone: str | None
    email: str | None
    address: str | None
    registration_date: str | None
