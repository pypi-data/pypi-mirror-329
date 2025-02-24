"""view all images."""

import pathlib
import typing as t

from matplotlib import pyplot as plt

from meterviewer import T

from ..img import process


def view_dataset_on_disk(name: str):
  def mmm(
    prefix_name: pathlib.Path,
    load_from_disk: t.Callable,
    view_dataset: t.Callable,
    show: bool = True,
    nums: int = 3,
  ):
    if not show:
      return

    assert prefix_name.exists()
    x = load_from_disk(prefix_name / name)
    x = process.np_to_img(x)
    view_dataset(nums, x)

  return mmm


def view_dataset_in_rows(num: int, imglist: T.ImgList):
  # 创建一个 GridSpec 实例，1行3列
  from matplotlib.gridspec import GridSpec

  fig = plt.figure(figsize=(15, 5))
  gs = GridSpec(1, 3, figure=fig)

  # 第一个子图
  ax1 = fig.add_subplot(gs[0, 0])
  ax1.imshow(imglist[0])

  # 第二个子图
  ax2 = fig.add_subplot(gs[0, 1])
  ax2.imshow(imglist[1])

  # 第三个子图
  ax3 = fig.add_subplot(gs[0, 2])
  ax3.imshow(imglist[2])

  plt.tight_layout()
  plt.show()


def view_dataset(num: int, imglist: T.ImgList):
  """显示图片列表中的图片"""
  if imgshape := len(imglist[0].shape) > 3:
    raise Exception(f"imglist or Dataset meets error, shape: {imgshape}")
  for im in imglist[:num]:
    plt.imshow(im)
    plt.show()
