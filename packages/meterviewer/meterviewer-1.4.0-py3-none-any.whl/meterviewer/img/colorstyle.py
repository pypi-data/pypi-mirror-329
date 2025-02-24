from meterviewer import types as T
import numpy as np
from PIL import Image


def to_gray(im: T.NpImage) -> T.NpImage:
  im = Image.fromarray(im).convert("L")
  return np.asarray(im)
