"""
test dataset functions.
"""

from __future__ import annotations

import functools
import pathlib

import pytest

from meterviewer import files
from meterviewer import types as T
from meterviewer.datasets import dataset
from meterviewer.datasets.read import single
from meterviewer.img import process
from tests.utils import show_img


def test_create_label():
  assert dataset.create_str_with_fill(1234, 5, 8) == [
    "0",
    "1",
    "2",
    "3",
    "4",
    "x",
    "x",
    "x",
  ]
  assert dataset.create_str_with_fill(12340, 5, 8) == [
    "1",
    "2",
    "3",
    "4",
    "0",
    "x",
    "x",
    "x",
  ]


def test_python_syntax():
  arr = ["1", "2", "3", "4"]
  arr.extend(["x"] * 3)
  assert arr == list("1234xxx")
  assert arr == ["1", "2", "3", "4", "x", "x", "x"]

  arr = list("1234")
  arr.extend(["x"] * 3)
  assert arr == list("1234xxx")


def test_fill_digit():
  assert dataset.fill_digit(list("12312"), 7) == list("12312xx")
  assert dataset.fill_digit(list("01234"), 8) == list("01234xxx")
  assert dataset.fill_digit(["0", "1", "2", "3", "4"], 8) == [
    "0",
    "1",
    "2",
    "3",
    "4",
    "x",
    "x",
    "x",
  ]
  assert list("12312xx") == ["1", "2", "3", "1", "2", "x", "x"]
  assert list("1212xx") == ["1", "2", "1", "2", "x", "x"]
  assert list("0123") == ["0", "1", "2", "3"]

  with pytest.raises(ValueError):
    dataset.fill_digit(list("12312"), 4)
    dataset.fill_digit(list("12"), 4)


def test_view_on_disk(root_path):
  f = dataset.view_dataset_on_disk(T.x_name)
  f(
    prefix_name=root_path / r"generated",
    load_from_disk=files.load_from_disk,
    view_dataset=dataset.view_dataset,
    show=True,
  )


def test_create_dataset(root_path):
  P = functools.partial

  def read_rand_img(digit: int | str):
    return single.read_rand_img(
      digit=digit,
      root=root_path,
      get_dataset=lambda: "M1L1XL",
    )

  gen_block = P(
    dataset.generate_block_img,
    join_func=dataset.join_with_resize,
    read_rand_img=read_rand_img,
  )

  path = root_path / pathlib.Path(r"generated")
  path.mkdir(exist_ok=True)

  filesave = P(
    files.save_img_labels_with_default,
    prefix_name=path,
    save_to_disk=files.save_to_disk,
  )

  def check_imgs(imglist):
    size = imglist[0].shape
    show_img(imglist[0])
    imgs = process.resize_imglist(imglist)
    for im in imgs:
      show_img(im)
      assert size == im.shape

  fn = dataset.create_dataset_func(check_imgs=lambda x: None, total=9)
  imgs, labels = fn(length=5, nums=10, gen_block_img=gen_block)
  filesave(imgs=imgs, labels=labels)


def test_generate_block_img(root_path):
  def read_rand_img(digit: int | str):
    return single.read_rand_img(
      digit=digit,
      root=root_path,
      get_dataset=lambda: "M1L1XL",
    )

  im = dataset.generate_block_img(
    ["1", "2", "3", "4"],
    process.join_img,
    read_rand_img,
  )
  show_img(im)

  im = dataset.generate_block_img(
    ["1", "2", "3", "5", "6"],
    dataset.join_with_resize,
    read_rand_img,
  )
  show_img(im)

  im = dataset.generate_block_img(
    ["1", "2", "3", "5", "6", "x", "x"],
    dataset.join_with_resize,
    read_rand_img,
  )
  show_img(im)


def test_get_random_dataset(root_path):
  _, index = dataset.get_random_dataset(root_path, dataset.get_dataset_list)
  assert index in range(0, 74)


def test_read_random_img(root_path):
  im = single.read_rand_img(root_path, lambda: "M1L1XL", 5)
  show_img(im)

  im = single.read_rand_img(root_path, lambda: "M1L1XL", "x")
  show_img(im)


def test_read_random_digit(root_path):
  path_gen = single.read_single_digit(root_path, lambda: "M1L1XL", 0, promise=False)()
  p = next(path_gen)
  assert pathlib.Path(p).exists()


def test_dataset_list(root_path):
  # path = root_path / pathlib.Path("lens_6/XL/XL")
  count = 0
  pics = []

  def update_count(name):
    nonlocal count, pics
    pics.append(name)
    count += 1

  dataset.handle_datasets(root_path, update_count)
  assert count == 74
  # assert False, pics
