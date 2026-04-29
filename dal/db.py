import sqlite3
from pathlib import Path


DB_PATH = Path("database") / "library.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Reader (
        ReaderID INTEGER PRIMARY KEY AUTOINCREMENT,
        FullName TEXT NOT NULL,
        Phone TEXT,
        Email TEXT,
        Address TEXT,
        RegistrationDate TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Author (
        AuthorID INTEGER PRIMARY KEY AUTOINCREMENT,
        FullName TEXT NOT NULL,
        BirthDate TEXT,
        Country TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Genre (
        GenreID INTEGER PRIMARY KEY AUTOINCREMENT,
        GenreName TEXT NOT NULL UNIQUE,
        Description TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Publisher (
        PublisherID INTEGER PRIMARY KEY AUTOINCREMENT,
        PublisherName TEXT NOT NULL UNIQUE,
        City TEXT,
        Phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Librarian (
        LibrarianID INTEGER PRIMARY KEY AUTOINCREMENT,
        LibrarianName TEXT NOT NULL,
        Position TEXT,
        Phone TEXT,
        Email TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Book (
        BookID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        ISBN TEXT,
        PublishYear INTEGER,
        CopiesAvailable INTEGER NOT NULL CHECK (CopiesAvailable >= 0),
        GenreID INTEGER NOT NULL,
        PublisherID INTEGER NOT NULL,
        FOREIGN KEY (GenreID) REFERENCES Genre(GenreID),
        FOREIGN KEY (PublisherID) REFERENCES Publisher(PublisherID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS BookAuthor (
        BookAuthorID INTEGER PRIMARY KEY AUTOINCREMENT,
        BookID INTEGER NOT NULL,
        AuthorID INTEGER NOT NULL,
        FOREIGN KEY (BookID) REFERENCES Book(BookID) ON DELETE CASCADE,
        FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID) ON DELETE CASCADE,
        UNIQUE(BookID, AuthorID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Loan (
        LoanID INTEGER PRIMARY KEY AUTOINCREMENT,
        ReaderID INTEGER NOT NULL,
        BookID INTEGER NOT NULL,
        LibrarianID INTEGER NOT NULL,
        IssueDate TEXT NOT NULL,
        DueDate TEXT NOT NULL,
        ReturnDate TEXT,
        Status TEXT NOT NULL,
        FOREIGN KEY (ReaderID) REFERENCES Reader(ReaderID),
        FOREIGN KEY (BookID) REFERENCES Book(BookID),
        FOREIGN KEY (LibrarianID) REFERENCES Librarian(LibrarianID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Reservation (
        ReservationID INTEGER PRIMARY KEY AUTOINCREMENT,
        ReaderID INTEGER NOT NULL,
        BookID INTEGER NOT NULL,
        ReservationDate TEXT NOT NULL,
        Status TEXT NOT NULL,
        FOREIGN KEY (ReaderID) REFERENCES Reader(ReaderID),
        FOREIGN KEY (BookID) REFERENCES Book(BookID)
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO Librarian (LibrarianID, LibrarianName, Position, Phone, Email)
    VALUES (1, 'Главный библиотекарь', 'Администратор', '+000000000', 'library@example.com')
    """)

    conn.commit()
    conn.close()
