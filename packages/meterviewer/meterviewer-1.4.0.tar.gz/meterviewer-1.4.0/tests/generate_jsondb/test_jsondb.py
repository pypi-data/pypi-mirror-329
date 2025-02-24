from pathlib import Path as _p

import pytest

from meterviewer.config import get_root_path
from meterviewer.generator import jsondb


def test_path():
  basic_path = get_root_path()
  assert basic_path.exists()

  def full_path(digit_num: int, is_test: bool):
    return basic_path / jsondb.get_mid_path(digit_num, is_test)

  for num, is_test in [(6, True), (6, False), (5, True), (5, False)]:
    f = full_path(num, is_test)
    assert full_path(num, True) != full_path(num, False), "test and train should be different"
    assert f.exists(), f"{f} does not exist."

  with pytest.raises(ValueError):
    full_path(7, True)
