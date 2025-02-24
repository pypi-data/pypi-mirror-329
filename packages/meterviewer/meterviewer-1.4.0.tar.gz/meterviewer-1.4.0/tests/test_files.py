import pathlib
import typing as t
import numpy as np
from meterviewer import files
from .utils import gen_img


def test_md5():
  res = files.compute_md5("src/tests/for_md5")
  assert res == "5093b7d2c218eaebde04b58b20491ef6"


def test_reshape():
  img = gen_img(size=(35, 25, 3))
  assert files.transform_img(img).shape == (1, 35, 25, 3)

  # test concat
  im1 = files.transform_img(img)
  im2 = files.transform_img(img)
  assert np.vstack([im1, im2, im2, im2]).shape == (4, 35, 25, 3)


def test_transform_label():
  label = ["1", "2", "3", "4", "5"]
  assert files.transform_label(label).shape == (1, 5)


def test_scan_pics(root_path):
  path = root_path / pathlib.Path(r"lens_6/XL/XL/M1L1XL/Digit/0")
  count = 0
  pics: t.List[pathlib.Path] = []

  def update_count(name):
    nonlocal count, pics
    pics.append(name)
    count += 1

  [update_count(name) for name in files.scan_pics(path)]
  assert count == 20
  assert pics[0].parent.name == "0"
  # path like this:
  # PosixPath('/home/svtter/Work/Dataset/MeterData/lens_6/XL/XL/M1L1XL/Digit/0/4_2018-11-23-19-21-01.jpg')
  # assert False, pics
