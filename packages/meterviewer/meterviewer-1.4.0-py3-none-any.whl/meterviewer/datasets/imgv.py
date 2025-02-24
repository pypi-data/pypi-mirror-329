"""view image and value, process md5 value."""

import pathlib
import typing as t
from pathlib import Path as P

import numpy as np
from loguru import logger
from matplotlib import pyplot as plt
from PIL import ImageFile
from tqdm import tqdm

from meterviewer import T
from meterviewer.datasets.read import config
from meterviewer.img import cmp

logger.add("./logs/meterviewer-proc.log")

# 修复 PIL 无法读取截断图片的问题; matplotlib 底层居然是 PIL？是我搞错了吗？
ImageFile.LOAD_TRUNCATED_IMAGES = True


def view_one_img_v(filepath: P) -> t.Tuple[T.NpImage, str, T.Rect]:
  """同时浏览图片和值"""
  im = plt.imread(str(filepath))
  v, rect = config.get_xml_config(filepath)
  return (im, v, rect)


hash_store = {}


def save_hash(im: T.NpImage, index: int):
  """save image file hash value."""
  hash = cmp.get_hash(im)
  res = hash_store.get(hash, None)
  if res is None:
    hash_store[hash] = index
  else:
    logger.error(f"Hash: {hash} is same with {res} and {index}")
    raise Exception("Img should not be same.")


def find_images(img_list: T.ImgList) -> int:
  logger.debug("start finding...")
  for i, img in tqdm(enumerate(img_list)):
    try:
      save_hash(img, i)
    except Exception as e:
      logger.warning(f"warning: {e} in {i}")
      return i
  # index in the np_path
  return -1


def find_hash_in_numpy(im: T.NpImage, np_path: pathlib.Path) -> int:
  save_hash(im, -1)
  x = np.load(np_path)
  res = find_images(list(x))
  return res
