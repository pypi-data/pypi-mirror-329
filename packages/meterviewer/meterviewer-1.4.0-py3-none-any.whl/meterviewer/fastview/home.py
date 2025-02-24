import streamlit as st

main_text = """
This tool-sets is built for quick process meter image data.

## Features

1. View Dataset

View the rectangle area of given image in dataset.

2. Download Configuration File

Download the configuration file of given image in dataset.

"""


def main():
  st.title("Meter data viewer")
  st.markdown(main_text)


if __name__ == "__main__":
  main()
