import ast
import os
import pathlib

import numpy as np
import pandas as pd
import streamlit as st
from meterviewer.config import get_root_path
from meterviewer.img import resize


def resize_app():
  st.title("Tool to resize images.")
  root_path = pathlib.Path("/home/xiuhao/work/Dataset/HRCdata")
  root_path = st.text_input("Enter the root path", value=str(root_path))
  root_path = pathlib.Path(root_path)

  path = st.text_input("Enter the path of the data", value="Train")
  st.text(os.listdir(root_path / path))

  x_name = st.text_input("Enter the value of x_name", value="x_train.original.npy")
  y_name = st.text_input("Enter the value of y_name", value="y_train.npy")
  output_name = st.text_input("Enter the output name", value="x_train.npy")

  folder_path = root_path / path
  x_path = folder_path / x_name
  y_path = folder_path / y_name

  x = np.load(x_path)
  y = np.load(y_path)
  st.text(f"x_shape: {x.shape}, y_shape: {y.shape}")

  size = st.text_input("Enter the new size of the image", value="(32, 300)")
  size = ast.literal_eval(size)
  if st.button("transform"):
    transform_state = st.text("transforming...")
    res = resize.resize_imglist(x, size)
    np.save(folder_path / output_name, res)
    transform_state.text("transformed!")


resize_app()
