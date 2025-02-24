# generate dataset path.
import os
import pathlib

import streamlit as st

from meterviewer.config import get_root_path


def main():
  st.title("Generate dataset path")
  p = get_root_path()
  p = pathlib.Path(st.text_input("root path:", value=p))
  dataset_name = st.selectbox("dataset name", options=os.listdir(p))

  ds_path = p / dataset_name
  st.button("finish")
  st.text(ds_path)


main()
