"""generate sqlite3 database"""

import typing as t
from pathlib import Path as P

from meterviewer import T, files
from meterviewer.datasets import dataset, imgv
from meterviewer.datasets.read import single
from meterviewer.models import littledb
from meterviewer.values import is_carry

from .base import Generator

# Type hint for database insertion function
dbInsertFunc = t.Callable[[str, int, bool], None]


def generate_for_one_dataset(dataset: P, insert: dbInsertFunc):
  """
  Process a single dataset and insert its image data into the database.

  Args:
      dataset (Path): Absolute path to the dataset directory
      insert (dbInsertFunc): Callback function to insert data into the database
          Expected signature: (image_path: str, value: int, is_carry: bool) -> None

  Raises:
      AssertionError: If dataset path is not absolute
  """
  assert dataset.is_absolute()
  for img_file in files.scan_pics(dataset):
    _, v, _ = imgv.view_one_img_v(img_file)
    # transform str to int
    val = int(v)

    insert(str(img_file), val, is_carry(v))


def generate_db_for_all(root: P, db_path: P):
  """
  Generate a single database containing data from all datasets.

  Args:
      root (Path): Root directory containing all datasets
      db_path (Path): Relative path where the database should be created

  Raises:
      AssertionError: If db_path is absolute
  """
  # insert to one database.
  assert not db_path.is_absolute()

  insert, _ = littledb.create_db(str(db_path))

  def generate_one(dataset: P):
    return generate_for_one_dataset(single.get_dataset_path(root, str(dataset)), insert)

  dataset.handle_datasets(
    root,
    generate_one,
  )


def create_db(root_path: P):
  """
  Create separate databases for each dataset in the root directory.
  Each database will be named 'items.db' and placed in its respective dataset directory.

  Args:
      root_path (Path): Root directory containing all datasets
  """
  db_name = "items.db"

  def handle_dataset(dataset_name: P):
    dataset_path = dataset.get_dataset_path(root_path, str(dataset_name))
    littledb.create_db(str(dataset_path / db_name))

  dataset.handle_datasets(
    root_path,
    handle_func=handle_dataset,
  )


class DB(Generator):
  """generate sqlite3 database"""

  def load_root_path(self):
    raise NotImplementedError("load_root_path")

  def create_db(self):
    return create_db(self.load_root_path())

  def generate_db_for_all(self, db_path: P):
    return generate_db_for_all(self.load_root_path(), db_path)

  def generate_for_one_dataset(self, dataset: P, insert: dbInsertFunc):
    return generate_for_one_dataset(dataset, insert)
