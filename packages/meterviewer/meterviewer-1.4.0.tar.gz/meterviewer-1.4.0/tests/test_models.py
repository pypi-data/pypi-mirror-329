from meterviewer.generator import db
from meterviewer.models import func
from pathlib import Path as P
import shutil
import pytest


def use_temp_db() -> P:
  dbpath = P("./alldata.db")
  new_db = dbpath.with_stem("alldata-temp")
  shutil.copy(dbpath, new_db)
  return new_db


def test_update_item():
  newdb = use_temp_db()
  func.update_item(newdb, 1, 2)

  item = func.get_first_item(newdb)
  assert item.carry_num == 2


@pytest.mark.skip("large database copy.")
def test_update_schema(remove_files):
  new_db = use_temp_db()

  func.update_schema(new_db)
  item = func.get_first_item(new_db)
  assert item.carry_num is None


def test_get_carry_items():
  items = func.get_carry_items(P("./alldata.db"))
  for item in items:
    assert item.is_carry == 1


def test_get_item():
  item = func.get_first_item(P("./alldata.db"))
  assert item.id == 1
