"""根据数值判断进位情况；与数值相关的函数"""

import typing as t
from . import types as T


def is_carry(val: str) -> bool:
  return val[-1] in ("0", "9")


def is_carry_over(digit: T.DigitInt) -> bool:
  if digit[-1] == 0 or digit[-1] == 9:
    return True
  return False


def make_full(arr: t.List, length: int):
  new_arr = arr.copy()
  if len(arr) <= length:
    new_arr = [False] * (length - len(arr)) + new_arr
  else:
    raise ValueError(f"length is too short, len(arr) == {len(arr)}")
  return new_arr


def get_carry_array(digit: T.DigitStr) -> t.List[bool]:
  """get digit array from given digit string"""
  assert len(digit) >= 5
  res = []
  # 不是进位
  if not is_carry("".join(digit)):
    return make_full(res, len(digit))
  else:
    res.append(True)  # last digit is 0 or 9
    for c in reversed(digit[:-1]):
      res.append(True)
      if not c == "9":  # not continue when not 9
        break

  res = make_full(res, len(digit))
  return res


# def label_check(label: T.Label):
#     pass
