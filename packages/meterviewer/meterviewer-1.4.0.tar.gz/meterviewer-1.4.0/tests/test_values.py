from meterviewer import values
import pytest


def test_is_carry():
  assert values.is_carry("123") is False
  assert values.is_carry("1239")
  assert values.is_carry("1230")


def test_make_full():
  assert values.make_full([1, 2, 3], 6) == [False, False, False, 1, 2, 3]
  assert values.make_full([1, 2, 3], 3) == [1, 2, 3]
  assert values.make_full([], 3) == [False, False, False]

  with pytest.raises(ValueError):
    assert values.make_full([1, 2, 3], 2)


def test_get_carry_arr():
  assert values.get_carry_array(list("123132")) == [False] * 6
  assert values.get_carry_array(list("12909")) == [False, False, False, True, True]
  assert values.get_carry_array(list("12999")) == [False, True, True, True, True]
