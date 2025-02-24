import glob
import pathlib
import random
import typing as t

from . import config


def read_image_area(file_path: pathlib.Path) -> config.T.Rect:
  """读取一个图片的长条矩形部分"""
  assert file_path.suffix in (".jpg", ".jpeg"), f"仅支持jpg文件, given name: {file_path}"
  assert file_path.exists(), f"{file_path}文件不存在"

  xml_filepath = config.get_xml_config_path(file_path, types="block")
  assert xml_filepath.exists(), f"{xml_filepath}文件不存在"

  return config.read_rect_from_file(xml_filepath, "block")


def get_random_image_file(root_dir: pathlib.Path) -> pathlib.Path:
  """获取随机图像文件"""
  return random.choice(list(root_dir.glob("*.jpg")))


def read_area_img(
  root: pathlib.Path,
  get_dataset: t.Callable[[], t.Union[str, pathlib.Path]],
  # range_: tuple[float, float],
  promise=False,
):
  pass


def list_images(root: pathlib.Path, dataset_name: str) -> list[pathlib.Path]:
  dataset_full_path = f"lens_6/XL/XL/{dataset_name}"
  return glob.glob(str(root / dataset_full_path / "*.jpg"))
