import pathlib

import pytest

from meterviewer.datasets.read import detection

sample_dataset = "M1L3XL"


def select_one(root_path, dataset_name: str) -> pathlib.Path:
  """第一个图片"""
  return pathlib.Path(detection.list_images(root_path, dataset_name)[0])


def test_read_to_get(root_path):
  res = detection.read_image_area(
    select_one(root_path, sample_dataset),
  )
  assert res is not None
  assert res["xmin"] is not None


def test_list_imgs(root_path):
  assert len(detection.list_images(root_path, "M1L3XL")) > 0
