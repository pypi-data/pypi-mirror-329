from __future__ import annotations
from meterviewer.models.littledb import get_session, Item
from pathlib import Path as P
from sqlalchemy import ScalarResult, select, text, update


def get_first_item(dbpath: P) -> Item:
  session = get_session(str(dbpath))
  stmt = select(Item).where(Item.id == 1)
  result = session.execute(stmt)
  return result.scalar_one()


def get_carry_items(dbpath: P | str) -> ScalarResult[Item]:
  # get items with is_carry == 1
  session = get_session(dbpath)
  stmt = select(Item).where(Item.is_carry == 1)
  result = session.execute(stmt)
  return result.scalars()


def update_schema(dbpath: P):
  # add column carry_num to Item
  session = get_session(str(dbpath))
  session.execute(text("ALTER TABLE Item ADD COLUMN carry_num INTEGER"))
  session.commit()


def update_item(dbpath: P, id: int, carry_num: int):
  session = get_session(dbpath)
  if carry_num != 0:
    session.execute(update(Item).where(Item.id == id).values(carry_num=carry_num))
  else:
    session.execute(
      update(Item).where(Item.id == id).values(carry_num=carry_num, is_carry=0)
    )
  session.commit()
