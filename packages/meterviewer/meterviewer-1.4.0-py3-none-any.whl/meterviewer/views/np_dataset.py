from __future__ import annotations

import pathlib
import typing as t

from meterviewer import files
from meterviewer import types as T
from meterviewer.datasets import dataset


def view_merge_np(
  current_dataset: str | pathlib.Path,
  view_dataset: t.Callable[[int, T.ImgList], None] = dataset.view_dataset,
  get_x_y: T.NameFunc = lambda: (T.x_name, T.y_name),
):
  """查看已处理的数据集

  Args:
      current_dataset: 数据集路径
      view_dataset: 用于查看数据集的回调函数
      get_x_y: 获取X和Y文件名的函数
  """
  pp = pathlib.Path(current_dataset)

  x_name, _ = get_x_y()
  view_func = dataset.view_dataset_on_disk(x_name)

  view_func(
    prefix_name=pp,
    view_dataset=view_dataset,
    load_from_disk=files.load_from_disk,
  )


def read_details(current_dataset: str) -> t.Optional[t.Dict]:
  """读取数据集的详细信息

  Args:
      current_dataset: 数据集路径

  Returns:
      包含数据集详细信息的字典，如果文件不存在则返回None
  """
  return files.read_toml(pathlib.Path(current_dataset) / "details.gen.toml")


def get_x_y_name() -> t.Tuple[str, str]:
  """获取默认的X和Y文件名

  Returns:
      包含X和Y文件名的元组
  """
  return T.x_name, T.y_name


def write_details(
  current_dataset: str | pathlib.Path,
  get_xy_name: T.NameFunc = get_x_y_name,
):
  """写入数据集的详细信息

  Args:
      current_dataset: 数据集路径
      get_xy_name: 获取X和Y文件名的函数
  """
  pp = pathlib.Path(current_dataset)

  def write_to_file(details, overwrite=True):
    p = pp / "details.gen.toml"
    if not overwrite and p.exists():
      print("Failed to write, file exists")
      return
    return files.write_toml(p, details)

  x_name, y_name = get_xy_name()

  dataset.show_details(
    get_x_train=lambda: files.load_from_disk(pp / x_name),
    get_y_train=lambda: files.load_from_disk(pp / y_name),
    get_details=lambda x, y: dataset.get_details(pp, x, y),
    write_to_file=write_to_file,
  )


class NPView(object):
  def view(self, current_dataset: str | pathlib.Path, default_way=1):
    if default_way == 1:
      view_func = self.view_dataset
    else:
      view_func = self.view_dataset_in_rows

    return view_merge_np(
      current_dataset=current_dataset,
      view_dataset=view_func,
      get_x_y=self.get_x_y_name,
    )

  def view_dataset(self, num: int, imglist: T.ImgList):
    return dataset.view_dataset(num, imglist)

  def view_dataset_in_rows(self, num: int, imglist: T.ImgList):
    return dataset.view_dataset_in_rows(num, imglist)

  def get_x_y_name(self):
    return T.x_name, T.y_name
