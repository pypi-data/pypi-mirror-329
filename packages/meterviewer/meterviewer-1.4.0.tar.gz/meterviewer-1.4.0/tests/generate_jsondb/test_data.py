import os
import pathlib

from meterviewer.generator.jsondb import get_base_dir, get_random_data


def test_get_random_data(set_config):
  data = get_random_data(is_relative_path=False)
  assert pathlib.Path(data).exists()

  data_path = get_random_data(is_relative_path=True)
  assert os.path.exists(get_base_dir() / data_path)
