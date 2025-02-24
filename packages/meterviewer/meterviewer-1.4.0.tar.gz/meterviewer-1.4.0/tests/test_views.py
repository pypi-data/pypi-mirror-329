from meterviewer.datasets import imgv
from meterviewer.views import np_dataset
from tests.utils import show_img


def test_view_merge_np(root_path):
  """test view_merge_np"""
  d = root_path / "generated"
  np_dataset.view_merge_np(d)
  assert True


def test_view_imgv(root_path):
  """test view_imgv"""
  img_path = root_path / "lens_6/XL/XL/M1L3XL/2018-11-23-12-16-01.jpg"
  # assert False, img_path
  im, v, rect = imgv.view_one_img_v(img_path)
  show_img(im)
  assert v == "000994"
