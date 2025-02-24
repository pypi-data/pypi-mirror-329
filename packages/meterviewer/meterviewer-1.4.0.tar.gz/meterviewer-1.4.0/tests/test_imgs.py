from pathlib import Path as P

from meterviewer import types as T
from meterviewer.datasets import imgv
from meterviewer.img import cut, draw, process


def test_cut(root_path):
  img_path = root_path / "lens_6/XL/XL/M1L3XL/2018-11-23-12-16-01.jpg"
  im = process.plt.imread(img_path)

  """<xmin>82</xmin>
			<ymin>39</ymin>
			<xmax>112</xmax>
			<ymax>72</ymax>"""

  rect = T.Rect(xmin=82, ymin=39, xmax=112, ymax=72)
  cut_img = cut.cut_img(im, rect)
  process.show_img(cut_img, is_stop=0)


def test_draw(root_path):
  img_path = root_path / "lens_6/XL/XL/M1L3XL/2018-11-23-12-16-01.jpg"
  im, v, rect = imgv.view_one_img_v(img_path)
  im = draw.draw_rectangle(im, rect)
  process.show_img(im, is_stop=0)


def test_draw_text(root_path):
  img_path = root_path / "lens_6/XL/XL/M1L3XL/2018-11-23-12-16-01.jpg"
  im, v, _ = imgv.view_one_img_v(img_path)
  im = draw.draw_text(im, v)
  process.show_img(im, is_stop=0)
