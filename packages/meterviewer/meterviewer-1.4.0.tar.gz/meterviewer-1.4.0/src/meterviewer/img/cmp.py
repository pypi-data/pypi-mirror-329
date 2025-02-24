# compare two image
import hashlib

from meterviewer import types as T


def comp_ims(im1: T.NpImage, im2: T.NpImage) -> bool:
  """对比图片内容看是否完全一致"""
  return get_hash(im1) == get_hash(im2)


def get_hash(img: T.NpImage) -> bytes:
  return hashlib.md5(img.tobytes()).digest()
