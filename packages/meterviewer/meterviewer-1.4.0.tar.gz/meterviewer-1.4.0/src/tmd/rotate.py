# rotate image.
import os
import pathlib
import typing as t

import numpy as np
import streamlit as st

from meterviewer.config import get_root_path
from tmd.dataset import NumpyDataset

try:
  import torch
  from torchvision.transforms import v2
except ImportError:
  st.text("Please install torch and torchvision.")

torch.manual_seed(17)


def trans_function():
  trans = torch.nn.Sequential(
    v2.Pad(10, fill=0, padding_mode="constant"),
    v2.RandomRotation(30),
    # v2.RandomResizedCrop(size=(224, 224), antialias=True),
    v2.RandomHorizontalFlip(p=0.5),
    # transforms.CenterCrop(10),
    v2.ColorJitter(),
  )
  return trans


def rotate():
  st.title("rotate the image.")
  root_path = get_root_path()
  root_path = st.text_input("Enter the root path", value=str(root_path))
  root_path = pathlib.Path(root_path)

  path = st.text_input("Enter the path of the data", value="generated_merged")
  st.text(os.listdir(root_path / path))

  num = st.text_input("Enter the number of data")
  x_name = st.text_input("Enter the value of x_name", value="x_test.npy")
  y_name = st.text_input("Enter the value of y_name", value="y_test.npy")

  try:
    num_v: int = int(num)
  except ValueError:
    st.text("Please enter a number")

  folder_path = root_path / path
  x_path = folder_path / x_name
  y_path = folder_path / y_name

  status = st.text("loading dataset...")
  ds = NumpyDataset(
    folder_path,
    x_path,
    y_path,
    transform=trans_function(),
  )
  status.text("Done.")

  if st.button("Transform"):
    x, y = ds[num_v]
    st.text(f"x_shape: {x.size}, y_shape: {y.shape}")

    st.image(x, caption=f"Meterdata {num}")
    st.text(f"Meterdata {num} is {y}")


if __name__ == "__main__":
  rotate()
