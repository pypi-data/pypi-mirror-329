"""
read data from disk.

处理单个数字数据集的函数，数据集格式为 `dataset_name/[0-9]`
"""

from __future__ import annotations

import pathlib
import random
import typing as t

from loguru import logger
from matplotlib import pyplot as plt

from meterviewer import T, files, func
from meterviewer.img import process

from ..dataset import get_dataset_path


def path_fusion(
  root: pathlib.Path,
  dataset_name: str,
  num: int,
):
  """生成单个数字图像的路径
  Args:
      root: 根目录路径
      dataset_name: 数据集名称
      num: 数字(0-9)
  Returns:
      对应数字图像的完整路径
  """
  p = get_dataset_path(root, dataset_name) / "Digit" / str(num)
  return p


def read_rand_img(
  root: pathlib.Path,
  get_dataset: t.Callable[[], t.Union[str, pathlib.Path]],
  digit: t.Union[int, str],
  promise=False,
) -> T.NpImage:
  """随机读取一张数字图像，单字
  Args:
      root: 根目录路径
      get_dataset: 获取数据集名称的函数
      digit: 要读取的数字或'x'(表示空白图像)
      promise: 是否确保路径存在
  Returns:
      随机选择的数字图像数组
  Raises:
      Exception: 当数据集中没有图像时抛出异常
  """
  if digit == "x":
    im = process.gen_empty_im((32, 40, 3))
    return im

  get_one = read_single_digit(
    root,
    get_dataset=get_dataset,
    num=int(digit),
    promise=promise,
  )
  all_imgs = list(get_one())
  length = len(all_imgs)

  if length == 0:
    raise Exception(f"Dataset contains no images, dataset: {get_dataset()}")

  i = random.randint(0, length - 1)
  im = plt.imread(all_imgs[i])
  return im


def read_single_digit(
  root_path: pathlib.Path,
  get_dataset: t.Callable[[], str | pathlib.Path],
  num: int,
  promise: bool,
) -> t.Callable[[], t.Iterator[pathlib.Path]]:
  """读取单个数字的所有图像
  Args:
      root_path: 根目录路径
      get_dataset: 获取数据集名称的函数
      num: 要读取的数字(0-9)
      promise: 是否确保路径存在
  Returns:
      返回一个生成器函数，用于遍历该数字的所有图像路径
  Raises:
      AssertionError: 当数字不在0-9范围内时抛出
      Exception: 当找不到图像时抛出
  """
  assert num in range(0, 10), "num must be 0~9"

  def might_fail_func() -> pathlib.Path:
    return path_fusion(root_path, str(get_dataset()), num)

  if promise:
    p = func.try_again(
      15,
      might_fail_func,
      is_validate_func=lambda p: p.exists(),
      fail_message=f"cannot num: {num}",
    )
  else:
    p = might_fail_func()

  logger.debug(f"path: {p}")

  def yield_pics():
    gen = files.scan_pics(path=p)
    try:
      img = next(gen)
      yield img
    except StopIteration:
      raise Exception(f"no images found in dataset {p}")

  return yield_pics
