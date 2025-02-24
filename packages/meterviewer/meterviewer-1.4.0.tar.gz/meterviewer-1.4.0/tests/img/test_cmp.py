import numpy as np

from meterviewer.img import cmp


def test_two_data():
  im1 = np.random.rand(100, 100, 3) * 255
  im2 = im1.copy()

  im3 = np.random.rand(100, 100, 3) * 255
  assert cmp.comp_ims(im1, im2)
  assert not cmp.comp_ims(im1, im3)


def test_one_chanel():
  im1 = np.random.rand(100, 100, 1) * 255
  im2 = im1.copy()

  # imarray = np.random.rand(100,100,1) * 255
  assert cmp.comp_ims(im1, im2)
