# quick view of a dataset

import glob
import os

# import pathlib
# import numpy as np
# import pandas as pd
# from matplotlib import pyplot as plt
import streamlit as st

from meterviewer.config import get_root_path
from meterviewer.datasets import imgv
from meterviewer.datasets.read import config
from meterviewer.img import cut, draw

desc = """
用于快速查看图片以及矩形框
"""


def main():
  st.title("Quick Viewer of Meter dataset")
  st.markdown(desc)
  # data_path = pathlib.Path("/home/xiuhao/work/Dataset/MeterData/lens_5/XL/DATA")
  data_path = get_root_path()

  dataset_len_ = st.number_input("Dataset length", value=6)
  dataset_type = st.text_input("Dataset type", value="XL")

  # dataset_name = st.text_input("Dataset name", value="M4L1XL")
  dataset_folder = data_path / f"lens_{dataset_len_}" / dataset_type / dataset_type
  dataset_name = st.selectbox("Dataset name", options=os.listdir(dataset_folder))

  img_folder = dataset_folder / dataset_name
  img_list = glob.glob(str(img_folder / "*.jpg"))
  # st.text(os.listdir(img_folder))

  filename = st.selectbox("Choose a file", img_list)
  # filename = st.text_input("Enter the filename", value="2018-11-23-12-16-01.jpg")

  # if st.button("View"):
  im, v, rect = imgv.view_one_img_v(img_folder / filename)
  st.text(f"image shape: {im.shape}")
  st.image(im, caption=f"filename: {filename}")

  st.text("with rect")
  rect_im = draw.draw_rectangle(im, rect)
  st.image(rect_im, caption=f"with rect: {filename}")

  cutted = cut.cut_img(im, rect)
  st.image(cutted, caption=f"cutted: {filename}")

  xml_path = config.get_xml_config_path(img_folder / filename, "block")
  st.download_button(
    label="Download xml",
    data=open(xml_path, "rb"),
    file_name=xml_path.name,
    mime="application/xml",
  )


main()
