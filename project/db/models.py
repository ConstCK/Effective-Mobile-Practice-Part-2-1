from __future__ import annotations
import datetime
from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import EmailStr

from .config import Base
from .constants import BuyingStatus


class Author(Base):
    """Таблица с авторами книг"""
    __tablename__ = 'authors'

    author_id: Mapped[int] = mapped_column(primary_key=True)
    name_author: Mapped[str] = mapped_column(String(64))
    books: Mapped[list[Book]] = relationship(back_populates='author')


class Genre(Base):
    """Таблица с жанрами книг"""
    __tablename__ = 'genres'

    genre_id: Mapped[int] = mapped_column(primary_key=True)
    name_genre: Mapped[str] = mapped_column(String(32))
    books: Mapped[list[Book]] = relationship(back_populates='genre')


class Book(Base):
    """Таблица с книгами"""
    __tablename__ = 'books'

    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    price: Mapped[int]
    author_id: Mapped[int] = mapped_column(
        ForeignKey(column='authors.author_id', ondelete='CASCADE'))
    genre_id: Mapped[int] = mapped_column(
        ForeignKey(column='genres.genre_id', ondelete='CASCADE'))
    author: Mapped[Author] = relationship(back_populates='books')
    genre: Mapped[Genre] = relationship(back_populates='books')

    __table_args__ = (CheckConstraint(
        'price > 0', name='check_positive_price'),)


class City(Base):
    """Таблица с городами заказчиков книг"""
    __tablename__ = 'cities'

    city_id: Mapped[int] = mapped_column(primary_key=True)
    name_city: Mapped[str] = mapped_column(String(64))
    days_delivery: Mapped[int]
    clients: Mapped[Client] = relationship(back_populates='city')

    __table_args__ = (CheckConstraint('days_delivery >= 0',
                                      name='check_positive_delivery_days'),)


class Client(Base):
    """Таблица с заказчиками книг"""
    __tablename__ = 'clients'

    client_id: Mapped[int] = mapped_column(primary_key=True)
    name_client: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(unique=True)
    city_id: Mapped[int] = mapped_column(ForeignKey(
        column='cities.city_id', ondelete='SET NULL'))
    city: Mapped[City] = relationship(back_populates='clients')
    buys: Mapped[Buy] = relationship(back_populates='client')


class Buy(Base):
    """Таблица с покупками книг"""
    __tablename__ = 'buys'

    buy_id: Mapped[int] = mapped_column(primary_key=True)
    buy_description: Mapped[str]
    client_id: Mapped[int] = mapped_column(ForeignKey(column='clients.client_id',
                                                      ondelete='CASCADE'))
    client: Mapped[Client] = relationship(back_populates='buys')


class Step(Base):
    """Таблица с этапами покупки книг"""
    __tablename__ = 'steps'

    step_id: Mapped[int] = mapped_column(primary_key=True)
    name_step: Mapped[BuyingStatus]


class BuyBook(Base):
    """Промежуточная таблица для связи таблиц с книгами и покупками"""
    __tablename__ = 'buy_book_association'

    buy_book_id: Mapped[int] = mapped_column(primary_key=True)
    buy_id: Mapped[int] = mapped_column(
        ForeignKey('buys.buy_id', ondelete='CASCADE'))
    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.book_id', ondelete='CASCADE'))
    amount: Mapped[int]

    __table_args__ = (CheckConstraint('amount > 0',
                                      name='check_positive_amount'),
                      UniqueConstraint('book_id', 'buy_id'),)


class BuyStep(Base):
    """Промежуточная таблица для связи таблиц с покупками и этапами"""
    __tablename__ = 'buy_step_association'

    buy_step_id: Mapped[int] = mapped_column(primary_key=True)
    buy_id: Mapped[int] = mapped_column(
        ForeignKey('buys.buy_id', ondelete='CASCADE'))
    step_id: Mapped[int] = mapped_column(
        ForeignKey('steps.step_id', ondelete='CASCADE'))
    date_step_beg: Mapped[datetime.datetime]
    date_step_end: Mapped[datetime.datetime]

    __table_args__ = (UniqueConstraint('step_id', 'buy_id'),)
