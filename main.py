from datetime import date, datetime

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

TEST = 1

if TEST:
    engine = create_engine('sqlite:///:memory:', echo=True)
else:
    engine = create_engine('sqlite:///test.db', echo=True)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    __abstract__ = True


class Author(Base):
    __tablename__ = 'author'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    birth_year: Mapped[int] = mapped_column(nullable=False)
    books: Mapped[list["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    publication_year: Mapped[int] = mapped_column()
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))
    author: Mapped["Author"] = relationship(back_populates="books")
    loans: Mapped[list["Loan"]] = relationship(back_populates="book")

class Member(Base):
    __tablename__ = 'member'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    loans: Mapped[list["Loan"]] = relationship(back_populates="member")

class Loan(Base):
    __tablename__ = 'loan'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    member_id: Mapped[int] = mapped_column(ForeignKey('member.id'))
    loan_date: Mapped[datetime] = mapped_column(default=datetime.now)
    return_date: Mapped[date] = mapped_column(nullable=True)
    book: Mapped["Book"] = relationship(back_populates="loans")
    member: Mapped["Member"] = relationship(back_populates="loans")

Base.metadata.create_all(engine)

def create_author(name: str, birth_year: int):
    obj = Author(name=name, birth_year=birth_year)
    save(obj)

def create_book(title: str, publication_year: int, author_id:int):
    obj = Book(title=title, publication_year=publication_year, author_id=author_id)
    save(obj)

def create_member(name: str, email: str):
    obj = Member(name=name, email=email)
    save(obj)

def create_loan(book_id: int, member_id: int):
    obj = Loan(book_id=book_id, member_id=member_id)
    save(obj)

#Добавление в Сессию
def add(obj, session: Session):
    session.add(obj)

#Открыть сессию -> Добавить объект
def save(obj):
    with Session(autoflush=False) as session:
        try:
            add(obj, session)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise


create_author("Tolstoy", 1828)
create_book("War and Peace", 1869, author_id=1)
create_member("Alice", "alice@example.com")
create_loan(book_id=1, member_id=1)
# Загружаем объекты
with Session(autoflush=False) as session:
    try:
        author = session.query(Author).first()
        book = session.query(Book).first()
        member = session.query(Member).first()
        loan = session.query(Loan).first()
        # Проверки связей
        assert author.name == "Tolstoy"
        assert book.title == "War and Peace"
        assert member.name == "Alice"

        assert book.author == author
        assert author.books[0] == book

        assert loan.book == book
        assert loan.member == member
        assert member.loans[0] == loan
    except SQLAlchemyError:
        raise



print("Все проверки пройдены ✅")





