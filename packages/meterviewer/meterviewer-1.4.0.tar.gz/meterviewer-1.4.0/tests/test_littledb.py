from meterviewer.models import littledb
from meterviewer.datasets import dataset
from pathlib import Path as P


def test_insert_one(root_path, remove_files):
  dataset_name = "M1L1XL"
  p = dataset.get_dataset_path(root_path, dataset_name)
  db = p / "items-temp.db"
  insert_one, _ = littledb.create_db(str(db))
  assert db.exists()

  insert_one("test", 0, False)

  # seems not work under windows
  remove_files(db)
  # db.unlink()


def test_create_db(root_path, remove_files):
  p = P("test.db")
  littledb.create_db(str(p))
  remove_files(p)

  p = P(root_path / "test.db")
  littledb.create_db(str(p))
  remove_files(p)
