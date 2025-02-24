import pytest
from meterviewer import func as F


def test_try_again():
  assert F.try_again(5, lambda: 1, lambda x: x == 1, fail_message="cannot get 1") == 1

  with pytest.raises(Exception):
    assert F.try_again(5, lambda: 1, lambda x: x == 2, fail_message="cannot get 1") == 1


def test_must_loop():
  def func(x):
    assert x == 1

  class LoopError(Exception):
    pass

  F.must_loop([1, 1, 1], func, LoopError)

  assert pytest.raises(LoopError, F.must_loop, [], func, LoopError)
