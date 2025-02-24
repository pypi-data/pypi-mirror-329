from PIL import Image
import streamlit as st
import pandas as pd
import pathlib
import numpy as np
from meterviewer.datasets import imgv
from matplotlib import pyplot as plt


def cmd():
  st.Page("compare page", title="Tool to compare images")
  root_path = pathlib.Path("/home/xiuhao/work/Dataset/HRCdata")
  dataset_1, dataset_2 = "Test", "Train"
  num = 1
  x1_name, x2_name = "x_all.npy", "x_train.npy"
  x1_path = root_path / dataset_1 / x1_name
  x2_path = root_path / dataset_2 / x2_name
  x1 = np.load(x1_path)
  x2: np.ndarray = np.load(x2_path)

  def save_img(path, arr):
    im = Image.fromarray(arr)
    im.save(path)

  im = x1[num]
  save_img("/tmp/im1.png", im)
  print("example saved.")

  inx = imgv.find_images(x2)
  if inx == -1:
    print("No same image found.")
  else:
    print(inx)
    print("Same image found.")
    save_img("/tmp/im2.png", x2[inx])


def main():
  st.title("Tool to compare images.")
  root_path = pathlib.Path("/home/xiuhao/work/Dataset/HRCdata")
  root_path = st.text_input("Enter the root path", value=str(root_path))
  root_path = pathlib.Path(root_path)

  dataset_1 = st.text_input("Enter the dataset 1 name", value="Test")
  dataset_2 = st.text_input("Enter the dataset 2 name", value="Train")

  num = st.text_input("Enter the number of data")
  x1_name = st.text_input("Enter the value of x1_name", value="x_all.npy")
  # y_name = st.text_input("Enter the value of y_name", value="y_test.npy")
  x2_name = st.text_input("Enter the value of x2_name", value="x_train.npy")

  try:
    data_load_state = st.text("reading data...")
    num = int(num)
    data_load_state.text("Done!")
  except ValueError:
    data_load_state.text("Please enter a number")
    return

  # folder_path = root_path / path
  x1_path = root_path / dataset_1 / x1_name
  x2_path = root_path / dataset_2 / x2_name

  assert x1_path.exists()
  assert x2_path.exists()

  x1 = np.load(x1_path)
  x2: np.ndarray = np.load(x2_path)

  st.text(f"x1_shape: {x1.shape}, x2_shape: {x2.shape}")

  st.text("Selected image: ")
  st.image(x1[num], caption=f"Meterdata {num}")

  # raise Exception("Not implemented yet")

  im = x1[num]
  if st.button("Search"):
    state = st.text("searching")
    inx = imgv.find_images(im, x2.tolist())
    if inx == -1:
      st.text("No same image found.")
    else:
      st.text("Same image found.")
      st.image(x2[inx], caption=f"Meterdata {inx}")
    state.text("finished")


if __name__ == "__main__":
  # cmd()
  main()
