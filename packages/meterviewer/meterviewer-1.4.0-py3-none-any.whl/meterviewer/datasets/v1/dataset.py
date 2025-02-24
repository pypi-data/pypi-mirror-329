# 统一数据集表示
# 只在一个文件里修改目录，方便快捷
# 将使用的函数放在参数上，减少依赖

from __future__ import annotations

import datetime
import os
import pathlib

# import numpy as np
import random
import typing as t

from tqdm import tqdm

from ... import files
from ... import types as T
from ...img import process
from ..join import join_with_fix, join_with_resize  # noqa
from ..view import view_dataset, view_dataset_in_rows, view_dataset_on_disk  # noqa


def generate_func() -> t.List[t.Callable[[pathlib.Path], T.ImgDataset]]:
  """生成一组用于加载数据集的函数

  Returns:
      返回一个函数列表,每个函数用于加载指定路径下的训练或测试数据
  """
  funcs = []
  names: t.List[str] = [T.x_name, T.y_name, T.x_test, T.y_test]
  for n in names:

    def get_func(path: pathlib.Path, name: str = n):
      return files.load_from_disk(path / name)

    funcs.append(get_func)

  return funcs


def get_details(
  path: pathlib.Path,
  x: T.ImgDataset,
  y: T.LabelData,
) -> t.Dict:
  """获取数据集的详细信息

  Args:
      path: 数据集路径
      x: 图像数据集
      y: 标签数据

  Returns:
      包含数据集详细信息的字典,包括路径、创建时间、数据形状等
  """
  data = {}

  def create_sub(name):
    data[name] = {}

  for name in ["Dataset", "Meta"]:
    create_sub(name)

  data["Dataset"]["path"] = str(path)
  data["Meta"]["config.create_time"] = datetime.datetime.now()
  data["Dataset"]["created_time"] = ""
  data["Dataset"]["updated_time"] = ""
  data["Dataset"]["x_shape"] = x.shape
  data["Dataset"]["y_shape"] = y.shape
  return data


def show_details(
  get_x_train,
  get_y_train,
  get_details: t.Callable[[t.Any, t.Any], t.Dict],
  write_to_file: t.Callable[[t.Dict], None],
):
  x, y = get_x_train(), get_y_train()
  details = get_details(x, y)
  write_to_file(details)


def dataset_length_list() -> t.List[int]:
  """返回支持的数字长度列表

  Returns:
      支持的数字位数列表[5,6,7,8]
  """
  return [5, 6, 7, 8]


def create_str_with_fill(
  number: int,
  length: int,
  total: int,
) -> T.DigitStr:
  """创建填充后的数字字符串

  Args:
      number: 要转换的数字
      length: 数字的长度
      total: 需要填充到的总长度

  Returns:
      填充后的数字字符串
  """
  return fill_digit(process.number_to_string(number, length), total)


def create_labels_func(
  length: int,
  total: int,
) -> t.Callable[[int], t.Tuple[t.List[int], t.List[T.DigitStr]]]:
  """创建标签生成函数

  Args:
      length: 数字长度
      total: 填充后的总长度

  Returns:
      返回一个函数,该函数生成指定数量的随机数字及其字符串表示
  """

  def generate_nums(train_nums: int):
    numbers = []
    str_digits = []
    for _ in range(train_nums):
      number = random.randint(0, 10**length)
      numbers.append(number)
      str_digits.append(
        create_str_with_fill(number, length, total),
      )
    return numbers, str_digits

  return generate_nums


class GenBlockImgFunc(t.Protocol):
  def __call__(self, digit: T.DigitStr) -> T.NpImage: ...


class SaveDatasetFunc(t.Protocol):
  def __call__(self, imgs: T.ImgList, str_digits: t.List[T.DigitStr]) -> None: ...


class CreateDatasetFunc(t.Protocol):
  def __call__(
    self,
    length: int,
    nums: int,
    gen_block_img: GenBlockImgFunc,
  ) -> t.Tuple[t.List[T.NpImage], t.List[T.DigitStr]]: ...


def create_dataset_func(
  check_imgs: t.Callable[[T.ImgList], None],
  total: int,
) -> CreateDatasetFunc:
  """创建数据集生成函数

  Args:
      check_imgs: 图像检查函数
      total: 填充后的总长度

  Returns:
      返回一个函数,用于生成包含指定数量和长度的数字图像数据集
  """

  def inner(
    length: int,
    nums: int,
    gen_block_img: GenBlockImgFunc,
  ):
    _, str_digits = create_labels_func(length, total)(nums)

    imgs = []
    for digit in tqdm(str_digits):
      im = gen_block_img(digit)
      imgs.append(im)

    # files.write_shape(imgs, 3)
    check_imgs(imgs)

    # automatic resize the images
    imgs = process.resize_imglist(imgs, size=[37, 297])
    return imgs, str_digits

  return inner


def get_random_dataset(
  root: pathlib.Path, get_dataset_list: t.Callable
) -> t.Tuple[pathlib.Path, int]:
  """随机获取一个数据集

  Args:
      root: 根目录
      get_dataset_list: 获取数据集列表的函数

  Returns:
      随机选择的数据集路径和索引
  """
  datasets = list(get_dataset_list(root))
  random_index = random.randint(0, len(datasets) - 1)
  return datasets[random_index], random_index


def generate_block_img(
  the_digit: T.DigitStr,
  join_func: T.JoinFunc,
  read_rand_img: t.Callable[[int | str], T.NpImage],
) -> T.NpImage:
  """生成数字块图像

  Args:
      the_digit: 数字字符串
      join_func: 图像拼接函数
      read_rand_img: 读取随机图像的函数

  Returns:
      拼接后的数字块图像
  """
  img_list = []
  for digit in the_digit:
    im = read_rand_img(digit)
    img_list.append(im)
  return join_func(img_list, process.size_check)


def get_dataset_path(root: pathlib.Path, dataset_name: str) -> pathlib.Path:
  """获取数据集路径

  Args:
      root: 根目录
      dataset_name: 数据集名称

  Returns:
      完整的数据集路径
  """
  p = root / "lens_6" / "XL" / "XL" / dataset_name
  return p


def get_dataset_list(
  root: pathlib.Path,
  default_func: t.Callable = lambda: pathlib.Path("lens_6/XL/XL"),
) -> t.Iterator[pathlib.Path]:
  """获取数据集列表

  Args:
      root: 根目录
      default_func: 默认路径生成函数

  Returns:
      数据集路径的迭代器
  """
  root = root / default_func()
  for dir in os.listdir(root):
    if os.path.isdir(root / dir):
      yield pathlib.Path(dir)


def handle_datasets(root: pathlib.Path, handle_func: t.Callable[[pathlib.Path], None]):
  """handle"""
  for dataset in get_dataset_list(root):
    handle_func(dataset)


def fill_digit(digit: T.DigitStr, total_length: int) -> T.DigitStr:
  """填充数字字符串到指定长度

  Args:
      digit: 原始数字字符串
      total_length: 目标长度

  Returns:
      填充后的数字字符串

  Raises:
      ValueError: 当输入字符串长度小于5或大于目标长度时
  """
  digit2 = digit.copy()
  if len(digit) < 5:
    raise ValueError(f"digit lenght must > 5, {digit}")

  if len(digit) <= total_length:
    digit2.extend(["x"] * (total_length - len(digit)))
  else:
    raise ValueError(f"digit lenght must < {total_length}, {digit}")
  return digit2
