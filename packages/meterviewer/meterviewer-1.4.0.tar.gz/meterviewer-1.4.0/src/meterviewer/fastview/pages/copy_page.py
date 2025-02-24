import streamlit as st
import pandas as pd
import pathlib
import numpy as np
import os
import ast
import shutil


def main():
  # st.Page("copy page", title="Tool to backup numpy")
  st.title("Tool to backup numpy.")
  root_path = pathlib.Path("/home/xiuhao/work/Dataset/HRCdata")
  root_path = st.text_input("Enter the root path", value=str(root_path))
  root_path = pathlib.Path(root_path)

  folder = st.text_input("Enter the path of the data", value="Train")

  st.text(os.listdir(root_path / folder))

  x_name = st.text_input("Enter the value of x_name", value="x_train.npy")
  y_name = st.text_input("Enter the value of y_name", value="y_train.npy")

  new_x_name = st.text_input(
    "Enter the value of new_x_name", value="x_train.original.npy"
  )
  new_y_name = st.text_input(
    "Enter the value of new_x_name", value="y_train.original.npy"
  )

  if st.button("Confirm"):
    shutil.copy(root_path / folder / x_name, root_path / folder / new_x_name)
    shutil.copy(root_path / folder / y_name, root_path / folder / new_y_name)


main()
