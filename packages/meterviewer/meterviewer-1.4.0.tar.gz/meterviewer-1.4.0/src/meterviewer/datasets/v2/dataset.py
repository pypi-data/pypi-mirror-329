# 统一数据集表示
# 只在一个文件里修改目录，方便快捷
# 将使用的函数放在参数上，减少依赖

from __future__ import annotations

import datetime
import os
import pathlib
import random
import typing as t

import numpy as np
from PIL import Image
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
  get_x_train: t.Callable,
  get_y_train: t.Callable,
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


def create_dataset_func(check_imgs: t.Callable[[T.ImgList], None]):
  def inner(
    root: pathlib.Path,
    dataset_list: t.List[str],
    available_digits: t.Dict[str, t.List[int]],  # 添加 available_digits 参数
    nums: int,
    gen_block_img: t.Callable[
      [pathlib.Path, t.List[str], t.Dict[str, t.List[int]], str],
      t.Tuple[T.NpImage, str],
    ],
    target_size: t.Tuple[int, int] = (297, 37),  # 目标尺寸
  ):
    imgs = []
    labels = []

    for _ in tqdm(range(nums)):
      digit = str(random.randint(0, 9))  # 随机选择数字
      img, new_label = gen_block_img(
        root, dataset_list, available_digits, digit
      )  # 传入 available_digits
      img_resized = Image.fromarray(img).resize(target_size)
      new_label_array = list(new_label)
      imgs.append(np.array(img_resized))
      labels.append(new_label_array)

    check_imgs(imgs)
    return imgs, labels

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


def scan_available_digits(
  root: pathlib.Path, dataset_list: t.List[str]
) -> t.Dict[str, t.List[int]]:
  """
  扫描数据集中实际包含的数字。

  Args:
      root: 数据集根目录
      dataset_list: 数据集名称列表

  Returns:
      每个数据集中实际可用数字的字典。
  """
  available_digits = {}
  for dataset_name in dataset_list:
    digit_dir = root / "lens_6" / "XL" / "XL" / dataset_name / "Digit"
    available_digits[dataset_name] = [
      int(digit.name)
      for digit in digit_dir.iterdir()
      if digit.is_dir() and digit.name.isdigit()
    ]
  return available_digits


def generate_block_img(
  root: pathlib.Path,
  dataset_list: t.List[str],  # 数据集名称列表
  available_digits: t.Dict[str, t.List[int]],  # 每个数据集中可用的数字
  digit: str,  # 用于随机数字选择的参数（可忽略）
  target_size: t.Tuple[int, int] = (37, 297),  # 目标尺寸 (高度, 宽度)
  left_replace_width: int = 147,  # 替换区域的总宽度
) -> t.Tuple[T.NpImage, str]:
  """
  从多个数据集中随机选择图像 A 和三个数字图像 B、C、D，
  替换图像 A 的前三位数字，生成新的图像 E 和对应的标签。
  第一位和第二位数字替换逻辑调整为数字 0 占比 38%。

  Args:
      root: 数据集根目录
      dataset_list: 数据集名称列表
      available_digits: 每个数据集中可用的数字
      digit: 不使用，仅占位
      target_size: 目标尺寸
      left_replace_width: 替换区域总宽度

  Returns:
      新生成的图像 E 和对应的标签。
  """

  def select_digit_with_probability(
    digits: t.List[int], probabilities: t.List[float]
  ) -> int:
    """
    根据给定的概率分布从数字列表中选择一个数字。

    Args:
        digits: 数字列表
        probabilities: 对应的概率分布

    Returns:
        选择的数字
    """
    return random.choices(digits, weights=probabilities, k=1)[0]

  # 随机选择数据集用于图像 A
  dataset_name_a = random.choice(dataset_list)
  image_block_dir = (
    root / "lens_6" / "XL" / "XL" / dataset_name_a / "ImageSets_block_zoom"
  )
  block_imgs = list(image_block_dir.glob("*.jpg"))
  if not block_imgs:
    raise Exception(f"No images found in {image_block_dir}")
  img_a_path = random.choice(block_imgs)
  img_a = Image.open(img_a_path).convert("RGB")

  # 从文件名解析 A 的标签
  img_a_label = img_a_path.stem.split("_")[2]

  # 调整图像 A 到目标尺寸
  img_a = np.array(Image.fromarray(np.array(img_a)).resize(target_size[::-1]))

  # 定义数字选择规则
  digits = list(range(10))  # 数字 0-9
  probabilities = [0.38] + [0.62 / 9] * 9  # 数字 0 占 38%，其余数字均匀分布

  # 替换图像的数字
  replacements = []
  for i in range(3):
    while True:
      dataset_name_b = random.choice(dataset_list)
      digits_for_dataset = available_digits.get(dataset_name_b, [])
      if digits_for_dataset:
        if i == 0:  # 第一位数字
          digit = select_digit_with_probability(digits, probabilities)
        elif i == 1:  # 第二位数字
          digit = select_digit_with_probability(digits, probabilities)
        else:  # 第三位数字，保持随机
          digit = random.choice(digits_for_dataset)

        # 检查数字是否存在于数据集
        if digit in digits_for_dataset:
          digit_img_dir = (
            root / "lens_6" / "XL" / "XL" / dataset_name_b / "Digit" / str(digit)
          )
          digit_imgs = list(digit_img_dir.glob("*.jpg"))
          if digit_imgs:
            img_b_path = random.choice(digit_imgs)
            img_b = Image.open(img_b_path).convert("RGB")
            replacements.append((str(digit), np.array(img_b)))
            break

  # 替换图像 A 的前三位数字
  section_width = left_replace_width // 3  # 每个数字的替换宽度
  for i, (digit, img_b) in enumerate(replacements):
    img_b_resized = np.array(
      Image.fromarray(img_b).resize((section_width, target_size[0]))
    )
    img_a[:, i * section_width : (i + 1) * section_width, :] = img_b_resized

  # 更新标签
  new_label = "".join([digit for digit, _ in replacements]) + img_a_label[3:]

  # 确保替换后的图像 E 是目标尺寸
  img_a = np.array(Image.fromarray(img_a).resize(target_size[::-1]))

  return img_a, new_label


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
