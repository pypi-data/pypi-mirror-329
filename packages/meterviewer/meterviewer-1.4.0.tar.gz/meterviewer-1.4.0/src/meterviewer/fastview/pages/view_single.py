import streamlit as st
import pandas as pd
import pathlib
import numpy as np
import os
from meterviewer.config import get_root_path


def our_app():
  st.title("Quick Viewer of Meterdata")
  root_path = get_root_path()
  root_path = st.text_input("Enter the root path", value=str(root_path))
  root_path = pathlib.Path(root_path)

  path = st.text_input("Enter the path of the data", value="generated_merged")
  st.text(os.listdir(root_path / path))

  num = st.text_input("Enter the number of data")
  x_name = st.text_input("Enter the value of x_name", value="x_test.npy")
  y_name = st.text_input("Enter the value of y_name", value="y_test.npy")

  try:
    data_load_state = st.text("reading data...")
    num = int(num)
    data_load_state.text("Done!")
  except ValueError:
    data_load_state.text("Please enter a number")
    return

  folder_path = root_path / path
  x_path = folder_path / x_name
  y_path = folder_path / y_name

  x = np.load(x_path)
  y = np.load(y_path)
  st.text(f"x_shape: {x.shape}, y_shape: {y.shape}")

  st.image(x[num], caption=f"Meterdata {num}")
  st.text(f"Meterdata {num} is {y[num]}")


our_app()
