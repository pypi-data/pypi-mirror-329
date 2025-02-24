"""create new generated dataset, generate all suitable images."""

import typing as t
from pathlib import Path as P

from PIL import Image

from meterviewer import T, files
from meterviewer.datasets import dataset, imgv
from meterviewer.datasets.read import config, single
from meterviewer.img import cut, process


def cut_one_img(filepath: P) -> t.Tuple[T.ImgList, T.DigitStr]:
  im, val, pos = imgv.view_one_img_v(filepath)
  xml_path = config.get_xml_config_path(filepath, "single")
  pos_list = config.read_rect_from_file(xml_path, "single")

  assert isinstance(pos_list, t.List)
  im_list = []
  for pos in pos_list:
    im1 = cut.cut_img(im, rect=pos.to_dict())
    im_list.append(im1)
  return im_list, list(val)


SaveFunc = t.Callable[[T.NpImage, str, int], t.Any]


def create_save_func(dataset_path: P, original_filepath: P) -> SaveFunc:
  assert dataset_path.exists(), f"the dataset: {dataset_path} should exist"

  def save_to_disk(im: T.NpImage, val: str, i: int):
    folder = dataset_path / val
    folder.mkdir(exist_ok=True)
    Image.fromarray(im).save(folder / f"{original_filepath.stem}_{i}.png")

  return save_to_disk


def cut_save_one(root_path: P, filepath: P):
  def cut_save(filepath: P, save_to_disk: SaveFunc):
    """切割图片并保存到磁盘上."""
    im_list, val = cut_one_img(filepath)
    for i, im in enumerate(im_list):
      save_to_disk(im, val[i], i)

  cut_save(filepath, create_save_func(root_path / "./generated", filepath))
