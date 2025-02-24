import glob
import pathlib

import cv2
import matplotlib.pyplot as plt

from meterviewer.datasets.read.config import get_xml_config
from meterviewer.datasets.read.detection import read_image_area
from meterviewer.img.draw import draw_rectangle


class MeterSet(object):
  def __init__(self, root_path: pathlib.Path, name: str):
    self.name = name
    self.root_path = root_path
    self.image_list: list[str] = []
    self.load_list()

  def images(self, i: int):
    if i > len(self.image_list):
      raise ValueError(f"index {i} out of range")
    return cv2.imread(self.image_list[i])

  def print_img(self, i: int, with_area: bool = False):
    img = self.images(i)
    if with_area:
      rect = self.pos(i)
      img = draw_rectangle(img, rect)
    plt.imshow(img)
    plt.show()

  def values(self, i: int):
    if i > len(self.image_list):
      raise ValueError(f"index {i} out of range")
    v, _ = get_xml_config(pathlib.Path(self.image_list[i]))
    return v

  def pos(self, i: int):
    if i > len(self.image_list):
      raise ValueError(f"index {i} out of range")
    filepath = self.image_list[i]
    rect = read_image_area(pathlib.Path(filepath))
    return rect

  def load_list(self):
    self.image_list = glob.glob(str(self.root_path / self.name / "*.jpg"))
