"""create jsondb for meter-viewer"""

import glob
import json
import os
import pathlib
import random
import typing as t
from functools import lru_cache

import toml
from pydantic import BaseModel

from meterviewer.datasets.read.detection import read_image_area

from .base import Generator
from .schema import Item, MeterDB


# cache config function (only read disk once), returns get_random_dataset and load_conf
def load_config(config_path: pathlib.Path) -> t.Callable[[], dict]:
  data: t.Optional[dict] = None

  def load_conf() -> dict:
    nonlocal data
    if data is None:
      with open(config_path, "r") as f:
        data = toml.load(f)
    assert data is not None, (config_path, data)
    return data

  return load_conf


get_local_config = None


# 随机选择一个数据集
def get_random_dataset(is_train: bool = True) -> str:
  dataset_list = get_dataset(is_train)
  return random.choice(dataset_list)


class DatasetList(BaseModel):
  digit_num: int
  dataset_list: list[str]


def _get_dataset(config, digit_number: int, is_train: bool = True) -> DatasetList:
  if is_train:
    key = "train_dataset"
  else:
    key = "test_dataset"

  if digit_number not in [5, 6]:
    raise ValueError(f"digit_number must be 5 or 6, but got {digit_number}")
  return DatasetList(
    digit_num=digit_number, dataset_list=config["base"][f"{digit_number}_digit"][key]
  )


# 获取数据集列表
def get_dataset(digit_number: int, is_train: bool = True) -> DatasetList:
  config = get_local_config()
  return _get_dataset(config, digit_number, is_train)


def _get_base_dir(config):
  return config["base"]["root_path"]


@lru_cache
def get_base_dir() -> str:
  """获取数据集的 base_dir"""
  config = get_local_config()
  return _get_base_dir(config)


@lru_cache
def get_mid_path(digit_num: int, is_test: bool) -> str:
  """获取数据集的 mid_path"""
  if digit_num not in [5, 6]:
    raise ValueError(f"digit_num must be 5 or 6, but got {digit_num}")

  if digit_num == 5:
    if is_test:
      return "lens_5/XL/DATA"
    else:
      return "lens_5/CS/Data_cs"
  if digit_num == 6:
    if is_test:
      return "lens_6/CS/all_CS"
    else:
      return "lens_6/XL/XL"
  raise ValueError(f"digit_num must be 5 or 6, but got {digit_num}")


def get_random_data(
  is_test: bool = False,
  is_relative_path: bool = True,
) -> pathlib.Path:
  """随机获取一个数据集下的图片"""
  dataset = get_random_dataset(is_train=not is_test)
  base_dir = get_base_dir()
  mid_path = get_mid_path(is_test=is_test)

  data_path = glob.glob(str(pathlib.Path(base_dir) / mid_path / dataset / "*.jpg"))
  random_path = random.choice(data_path)
  if is_relative_path:
    return pathlib.Path(random_path).relative_to(base_dir)
  else:
    return pathlib.Path(random_path)


# Not a pure function.
def set_local_config(infile: pathlib.Path):
  """设置本地配置, 只针对直接调用的函数有效"""
  global get_local_config
  get_local_config = load_config(config_path=infile)


def get_images_with_full_path(
  base_dir: str,
  dataset_name: str,
  digit_number: int,
  is_test: bool,
) -> list[str]:
  full_path = str(
    pathlib.Path(base_dir).expanduser()
    / get_mid_path(digit_number, is_test)
    / dataset_name
    / "*.jpg"
  )
  print("full_path: ", full_path)
  data_path = glob.glob(full_path)
  return data_path


def get_dataset_dir(
  digit_number: int,
  is_test: bool,
) -> pathlib.Path:
  return pathlib.Path(get_base_dir()) / get_mid_path(digit_number, is_test)


def gen_db(
  infile: pathlib.Path,
  output: pathlib.Path,
  stage: t.Literal["train", "test"],
):
  """
  读取数据集下所有的图片, 以及点的位置, 生成一个json文件
  """

  # set the get_local_config
  set_local_config(infile)

  data = []
  is_train = stage == "train"
  is_test = stage == "test"

  base_dir = get_base_dir()

  # 获取 5-6 位的大型数据集
  for digit in [6, 5]:
    dataset = get_dataset(digit, is_train)
    # 遍历小数据集，根据不同的仪表型号区分的

    for dataset_name in dataset.dataset_list:
      # 获取所有的图像路径
      img_paths = get_images_with_full_path(
        base_dir,
        dataset_name,
        dataset.digit_num,
        is_test,
      )

      if not img_paths:
        print(f"no image found for dataset: {dataset_name}, {img_paths}")
        continue

      for img_path in img_paths:
        assert os.path.exists(img_path), f"image not found: {img_path}"
        assert os.path.isfile(img_path), f"image is not a file: {img_path}"

        # 读取图像中的点
        rect = read_image_area(pathlib.Path(img_path))

        # 使用相对路径可以避免生成的 db 无法在其他机器上使用
        relative_path = pathlib.Path(img_path).relative_to(base_dir)

        item = Item(
          filepath=str(relative_path),
          dataset=dataset_name,
          xmin=rect["xmin"],
          xmax=rect["xmax"],
          ymin=rect["ymin"],
          ymax=rect["ymax"],
        )
        data.append(item)

  meter_db = MeterDB(data=data)

  with open(output, "w") as f:
    json.dump(meter_db.model_dump(), f)

  return output


class JSONDB(Generator):
  """generate jsondb, inherit get_local_config method to get local config"""

  def get_infile(self):
    raise NotImplementedError("get_infile")

  def get_local_config(self) -> dict:
    fn = load_config(config_path=self.get_infile())
    return fn()

  def get_dataset(self, digit_number: int, is_train: bool = True) -> DatasetList:
    return _get_dataset(self.get_local_config(), digit_number, is_train)

  def get_base_dir(self) -> str:
    """获取数据集的 base_dir"""
    config = self.get_local_config()
    return config["base"]["root_path"]
