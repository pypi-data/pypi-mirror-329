# 处理图像以适应训练要求

from __future__ import annotations

import sys
import typing as t

import numpy as np
from matplotlib import pyplot as plt

# from matplotlib import pyplot as plt
from .. import types as T
from .resize import check_img_size, resize_img, resize_imglist, size_check  # noqa


def np_to_img(data: np.ndarray) -> T.ImgList:
  """将numpy数组转换为图像列表"""
  return list(data)


def join_img(
  imglist: T.ImgList,
  check_func: t.Callable[[t.Any], t.Any],
) -> T.NpImage:
  """水平合并图像
  Args:
      imglist: 图像列表
      check_func: 检查函数
  Returns:
      合并后的numpy图像数组
  """
  check_func(imglist)
  return np.hstack(imglist)


def get_random_img(num: int, img_from: t.Callable) -> T.NpImage:
  """获取随机图像
  Args:
      num: 图像的数字位数
      img_from: 图像来源函数
  Returns:
      随机生成的numpy图像数组
  """
  get_img = img_from()
  return get_img(num)


def img_from(folder: str = ""):
  """从文件夹获取所有图像
  Args:
      folder: 图像文件夹路径
  Returns:
      获取图像的函数
  """

  def get_img(num):
    # 生成随机图像数组(10x20)，像素值范围1-255
    return np.random.randint(1, 255, size=(10, 20))

  return get_img


def get_img_list(nums: t.List[int]) -> t.List[T.NpImage]:
  """根据数字列表获取对应的图像列表
  Args:
      nums: 数字列表
  Returns:
      图像列表
  """
  imgs = []
  for i in nums:
    imgs.append(get_random_img(int(i), lambda: None))
  return imgs


def number_to_string(number: int, length: int) -> t.List[str]:
  """将数字转换为固定长度的字符串列表
  Args:
      number: 要转换的数字
      length: 期望的字符串长度
  Returns:
      字符串列表，不足位数用0填充
  """
  return list(str(number).zfill(length))


def empty_check(*args, **kwargs):
  """空检查函数，不执行任何操作"""
  pass


def gen_block_img(number: int, length: int):
  """在内存中生成图像块，用作示例函数
  Args:
      number: 要生成图像的数字
      length: 期望的长度
  Returns:
      合并后的图像块
  """
  num_l = [int(i) for i in number_to_string(number, length)]
  return join_img(get_img_list(num_l), empty_check)


def show_img(img, is_stop):
  """显示图像
  Args:
      img: 要显示的图像
      is_stop: 是否在显示后退出程序
  """
  plt.imshow(img)
  plt.show()
  if is_stop:
    sys.exit(-1)


def gen_empty_im(size: t.Tuple[int, int, int]):
  """生成指定大小的空白图像
  Args:
      size: 图像大小元组 (高度, 宽度, 通道数)
  Returns:
      空白图像数组
  """
  return np.zeros(size, dtype=np.uint8)
