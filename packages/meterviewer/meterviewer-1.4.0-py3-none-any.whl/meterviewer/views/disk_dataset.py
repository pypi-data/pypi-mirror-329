"""view the dataset"""

import pathlib
import random
import typing as t

import cv2

from meterviewer.generator import jsondb
from meterviewer.img import draw
from meterviewer.types import Rect


# 从数据集中随机获取一张图
def get_random_images(
  dataset: str,
  digit_num: int,
  stage: str,
  get_base_dir=jsondb.get_base_dir,
):
  images = jsondb.get_images_with_full_path(
    get_base_dir(),
    dataset,
    digit_num,
    is_test=stage == "test",
  )
  return images


# 生成样例数据图片列表的函数
def gen_plt_images(datasets: jsondb.DatasetList, digit_num: int, stage: str):
  # 输入 get_random_image 的函数
  def fn(get_random_image=get_random_image):
    plt_images = []
    for dataset in datasets.dataset_list:
      images = get_random_images(dataset, digit_num, stage)
      if len(images) == 0:
        print(f"empty dataset: {dataset}")
        continue

      item = {
        "dataset": (dataset, len(images)),
        "image": get_random_image(images),
      }
      plt_images.append(item)
    return plt_images

  return fn


# 根据数据集随机返回一张图片
def get_random_image_by_dataset(dataset: str, digit_num: int, stage: str):
  images = get_random_images(dataset, digit_num, stage)
  if len(images) == 0:
    raise ValueError(f"empty dataset: {dataset}")

  def fn(image: pathlib.Path):
    area = jsondb.read_image_area(image)
    area = Rect.model_validate(area)
    return area

  return get_random_image(images, read_image_area=fn)


# 随机抽取一张图片，画框
def get_random_image(
  images: list[str], read_image_area: t.Callable[[pathlib.Path], Rect]
):
  """
  draw random image from image list
  images: image list, full path
  """
  image = pathlib.Path(random.choice(images))
  area = read_image_area(image)
  im = cv2.imread(image)
  drawed_im = draw.draw_rectangle(im, area)
  print(area)
  return drawed_im


class DatasetView(object):
  """DatasetView"""

  def get_random_image_by_dataset(self, dataset: str, digit_num: int, stage: str):
    images = get_random_images(dataset, digit_num, stage, self.get_base_dir)
    self.check_images(images, dataset)
    return get_random_image(images, self.read_image_area)

  def check_images(self, images: list[str], dataset: str):
    if len(images) == 0:
      raise ValueError(f"empty dataset: {dataset}")

  def get_base_dir(self):
    return jsondb.get_base_dir()

  def read_image_area(self, image: pathlib.Path):
    area = jsondb.read_image_area(image)
    area = Rect.model_validate(area)
    return area
