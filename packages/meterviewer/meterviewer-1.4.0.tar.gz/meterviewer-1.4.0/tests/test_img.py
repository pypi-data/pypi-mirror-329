from meterviewer.img import process

# import functools
# from matplotlib import pyplot as plt
from tests.utils import show_img, gen_img


def test_resize_imglist():
  imglist = [gen_img(size=(35, 25, 3)), gen_img(size=(34, 25, 3))]
  process.resize_imglist(imglist, size=[35, 25])

  imglist = [gen_img(size=(31, 170, 3)), gen_img(size=(31, 175, 3))]
  process.resize_imglist(imglist)


def test_resize_img():
  im = gen_img(size=(35, 25, 3))
  process.resize_img(im, size=[35, 25])


def test_number_to_string():
  assert process.number_to_string(1, 5) == list("00001")
  assert process.number_to_string(10, 5) == ["0", "0", "0", "1", "0"]
  assert process.number_to_string(100, 5) == list("00100")
  assert process.number_to_string(1000, 5) == list("01000")


def test_join():
  imglist = [
    process.get_random_img(1, process.img_from),
    process.get_random_img(2, process.img_from),
    process.get_random_img(3, process.img_from),
  ]
  res = process.join_img(imglist, process.empty_check)
  assert res.shape[1] > res.shape[0]
  # seems correct
  show_img(res)
