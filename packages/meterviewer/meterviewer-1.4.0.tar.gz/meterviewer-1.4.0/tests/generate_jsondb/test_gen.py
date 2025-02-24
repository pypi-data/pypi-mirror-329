import json
import os
import pathlib

import pytest

from meterviewer.generator.jsondb import gen_db, get_random_data
from meterviewer.generator.schema import MeterDB


@pytest.fixture
def gen(set_config):
  yield gen_db(infile=set_config, output=pathlib.Path(__file__).parent / "meterdb.json")
  os.unlink(pathlib.Path(__file__).parent / "meterdb.json")


def test_the_db(gen):
  assert gen.exists()


def test_db_content(gen):
  with open(gen, "r") as f:
    content = json.load(f)
  db = MeterDB.model_validate(content)
  assert len(db.data) > 0

  # we confirm that the data exists.
  data_path = str(get_random_data(is_relative_path=True))

  # test if the data exists in the db.
  find = False
  for item in db.data:
    if item.filepath == data_path:
      find = True
      break
  assert find
