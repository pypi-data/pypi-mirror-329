import typing as t
import numpy as np


class Validator(object):
  # a image validator

  def is_img(self, img: np.ndarray) -> bool:
    conds = [
      lambda x: isinstance(x, np.ndarray),
      lambda x: len(x.shape) == 3,  # gray and color.
      lambda x: x.dtype == np.uint8,
      lambda x: x.shape[2] in [1, 3],  # gray and color.
      lambda x: x.shape[0] > 0 and x.shape[1] > 0,
    ]
    for c in conds:
      if not c(img):
        return False
    return True

  def valid_shape(self, img: np.ndarray, shape: t.Tuple) -> bool:
    return img.shape == shape
