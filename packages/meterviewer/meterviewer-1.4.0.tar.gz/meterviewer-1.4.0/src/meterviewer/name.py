# 该模块用于管理数据集文件的命名规则
import typing as t

from meterviewer import types as T


def normal_x_y() -> t.Tuple[str, str]:
  """返回普通数据集的X和Y文件名

  Returns:
      tuple: 包含X数据文件名和Y数据文件名的元组
  """
  return "x.npy", "y.npy"


def train_x_y() -> t.Tuple[str, str]:
  """返回训练数据集的X和Y文件名

  Returns:
      tuple: 包含X训练数据文件名和Y训练数据文件名的元组
  """
  return T.x_name, T.y_name


# 文件命名函数的映射字典
name_funcs = {
  "normal": normal_x_y,  # 普通数据集命名函数
  "train": train_x_y,  # 训练数据集命名函数
}
