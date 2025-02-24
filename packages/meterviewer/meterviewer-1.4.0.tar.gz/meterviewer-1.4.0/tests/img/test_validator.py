import numpy as np

from meterviewer.img import validator


def test_validator():
  v = validator.Validator()

  cases = [
    (np.array([1, 2, 3]), False),
  ]
  for img, expected in cases:
    assert expected == v.is_img(img)
