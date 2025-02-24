import typing as t

import numpy as np
from pydantic import BaseModel

# Numpy typed Image
NpImage = np.ndarray

Label = np.ndarray
ImgSize = t.Union[t.List[int], t.Tuple[int, int]]

ImgDataset = np.ndarray
LabelData = np.ndarray


Func = t.Callable

ImgList = t.List[NpImage]
DigitStr = t.List[str]
DigitInt = t.List[int]

CheckFunc = t.Callable[[t.Any], t.Any]
JoinFunc = t.Callable[[ImgList, CheckFunc], NpImage]
NameFunc = t.Callable[[], t.Tuple[str, str]]

x_name: str = "x_train.npy"
y_name: str = "y_train.npy"
x_test: str = "x_test.npy"
y_test: str = "y_test.npy"


def isImgDataset(x: t.Any) -> bool:
  return isinstance(x, np.ndarray) and len(x.shape) == 4


def isLabelData(y: t.Any) -> bool:
  return isinstance(y, np.ndarray) and len(y.shape) == 2


class Rect(BaseModel):
  xmin: int
  ymin: int
  xmax: int
  ymax: int
