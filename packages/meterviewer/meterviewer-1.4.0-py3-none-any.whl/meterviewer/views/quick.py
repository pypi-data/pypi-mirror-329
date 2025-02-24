"""快速浏览 np 类型的数据集"""

from pathlib import Path as P

from meterviewer import files
from meterviewer import types as T

from . import np_dataset


def more_quick_view(
  current_dataset: P,
  write_config=True,
):
  """增强的快速查看功能，自动检测数据集类型

  Args:
      current_dataset: 数据集路径
      write_config: 是否写入配置文件

  Returns:
      tuple: 包含X数据和Y数据的元组
  """
  name_func = files.use_smart_name(current_dataset)
  return quick_view(str(current_dataset), name_func, write_config)


def quick_view(
  current_dataset: str,
  get_x_y_name: T.NameFunc,
  write_config=True,
):
  """快速查看数据集

  Args:
      current_dataset: 数据集路径
      get_x_y_name: 获取X和Y文件名的函数
      write_config: 是否写入配置文件

  Returns:
      tuple: 包含X数据和Y数据的元组
  """
  x_name, y_name = get_x_y_name()
  x = files.load_from_disk(P(current_dataset) / x_name)
  y = files.load_from_disk(P(current_dataset) / y_name)

  np_dataset.view_merge_np(current_dataset, get_x_y=get_x_y_name)
  if write_config:
    np_dataset.write_details(current_dataset, get_xy_name=get_x_y_name)
  return x, y


def fast_preview(current_dataset: P):
  """最简单的数据集预览函数

  Args:
      current_dataset: 数据集路径

  Returns:
      tuple: 包含X数据和Y数据的元组
  """
  return more_quick_view(current_dataset)
