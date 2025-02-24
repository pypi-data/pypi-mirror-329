from __future__ import annotations

import pathlib
import typing as t

import numpy as np
from PIL import Image

try:
  import torch
  from torch.utils.data import Dataset
  from torchvision import datasets
except ImportError:
  st.text("Please install torch and torchvision.")

# from torchvision.transforms import transforms


class NumpyDataset(Dataset):
  def __init__(
    self,
    root: pathlib.Path,
    x_name: str | pathlib.Path,
    y_name: str | pathlib.Path,
    transform: t.Optional[t.Callable] = None,
    target_transform: t.Optional[t.Callable] = None,
  ):
    self.x_name = x_name
    self.y_name = y_name
    self.x = np.load(root / x_name)
    self.y = np.load(root / y_name)
    self.transform = transform
    self.target_transform = target_transform

  def __getitem__(self, index: int) -> tuple[Image.Image, np.ndarray]:
    x = self.x[index]
    y = self.y[index]

    x = Image.fromarray(x)

    if self.transform:
      x = self.transform(x)
    if self.target_transform:
      y = self.target_transform(y)
    return x, y
