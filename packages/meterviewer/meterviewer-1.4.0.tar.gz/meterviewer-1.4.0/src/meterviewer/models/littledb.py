"""
create a little db for storing the images and values.

some basic models.
"""

from __future__ import annotations

import pathlib
import typing as t
from typing import List, Optional

from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship


def get_session(filepath: str | pathlib.Path):
  filepath = str(filepath)
  engine = create_engine(f"sqlite:///{filepath}", echo=True)
  with Session(engine) as session:
    return session


def create_db(filepath: str):
  engine = create_engine(f"sqlite:///{filepath}", echo=True)
  Base.metadata.create_all(engine)

  with Session(engine) as session:

    def insert_one(filename: str, value: int, is_carry: bool):
      item = Item(filename=filename, value=value, is_carry=is_carry)
      session.add(item)
      session.commit()

    def insert_all(items: t.List[Item]):
      session.add_all(items)
      session.commit()

    return insert_one, insert_all


class Base(DeclarativeBase):
  pass


class Item(Base):
  __tablename__ = "item"
  id: Mapped[int] = mapped_column(primary_key=True)
  filename: Mapped[str] = mapped_column(String(30))
  value: Mapped[int] = mapped_column()
  is_carry: Mapped[bool] = mapped_column()
  carry_num: Mapped[int] = mapped_column()

  def __repr__(self) -> str:
    return f"Item(id={self.id!r}, filename={self.filename!r}, value={self.value!r})"


# examples
def examples():
  class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
      back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
      return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

  class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
      return f"Address(id={self.id!r}, email_address={self.email_address!r})"
