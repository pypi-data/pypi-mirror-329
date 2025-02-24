import pathlib

import pytest

from meterviewer.generator.jsondb import set_local_config


@pytest.fixture
def set_config():
  config_path = pathlib.Path(__file__).parent / "config.toml"
  set_local_config(config_path)
  return config_path
