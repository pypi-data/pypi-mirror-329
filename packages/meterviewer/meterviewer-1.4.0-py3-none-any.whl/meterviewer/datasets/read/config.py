# read dataset from file system.
import typing as t
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path as P

from meterviewer import func as F
from meterviewer import types as T

from .types import typeOfrect


@dataclass
class RectO(object):
  """矩形对象类，用于存储和处理矩形框的坐标信息

  属性:
      xmin (str): 矩形左边界x坐标
      ymin (str): 矩形上边界y坐标
      xmax (str): 矩形右边界x坐标
      ymax (str): 矩形下边界y坐标
  """

  xmin: str = ""
  ymin: str = ""
  xmax: str = ""
  ymax: str = ""

  def check(self):
    # assert rect.xmin != "" and rect.ymin != "" and rect.xmax != "" and rect.ymax != "", rect
    assert (
      self.xmin != "" and self.ymin != "" and self.xmax != "" and self.ymax != ""
    ), self

  def to_dict(self) -> T.Rect:
    return T.Rect.model_validate(
      {
        "xmin": self.xmin,
        "ymin": self.ymin,
        "xmax": self.xmax,
        "ymax": self.ymax,
      }
    )

  def __str__(self):
    return f"RectO({self.xmin}, {self.ymin}, {self.xmax}, {self.ymax})"

  def __repr__(self):
    return self.__str__()


def read_rect_from_node(root: t.Iterable) -> t.Tuple[str, T.Rect]:
  """从XML节点中读取矩形框信息

  Args:
      root (Iterable): XML根节点

  Returns:
      Tuple[str, T.Rect]: 返回值和矩形框字典的元组
  """
  val, rect_dict = "", RectO()
  for child in root:
    # find object
    if not child.tag == "object":
      continue
    for subchild in child:
      if subchild.tag == "name":
        val = str(subchild.text)

      # print(subchild.tag, subchild.text)
      if subchild.tag == "bndbox":
        for sub in subchild:
          setattr(rect_dict, sub.tag, sub.text)

  return val, rect_dict.to_dict()


def read_xml(filename: P):
  """读取 xml 文件，获取 root 节点"""
  assert filename.exists(), f"{filename}文件不存在"
  tree = ET.parse(filename)
  return tree.getroot()


def read_xml_to_get(
  filename: P,
  read_func: t.Callable[[t.Any], t.Any] = read_rect_from_node,
):
  """读取并解析XML文件

  Args:
      filename (P): XML文件路径
      read_func (Callable): 用于处理XML根节点的回调函数

  Returns:
      Any: 回调函数的返回结果
  """
  assert filename.exists(), f"{filename}文件不存在"
  return read_func(read_xml(filename))


def read_single_digit_rect(filename) -> t.List[RectO]:
  """读取单个数字的矩形框信息

  Args:
      filename: XML文件路径

  Returns:
      List[RectO]: 包含6个数字位置的矩形框列表
  """

  def func(root: t.Iterable) -> t.List[RectO]:
    def find_no(node) -> t.Tuple[int, RectO]:
      no = -1
      rect = RectO()
      for subchild in node:
        if subchild.tag == "no":
          no = int(subchild.text.strip())
        else:
          rect = set_rect(rect, subchild)
      rect.check()
      assert no != -1, "cannot find no number"
      return no, rect

    def set_rect(rect: RectO, sub) -> RectO:
      assert hasattr(rect, sub.tag), (sub.tag, sub.text)
      setattr(rect, sub.tag, sub.text)
      assert getattr(rect, sub.tag) != ""
      return rect

    def num_check():
      seta = {0, 1, 2, 3, 4, 5}
      setb = set()

      def is_valid():
        return seta == setb, (seta, setb)

      def set_num(no):
        setb.add(no)

      return set_num, is_valid

    digit_rect = [RectO() for _ in range(6)]
    set_num, is_valid = num_check()
    is_loop, set_loop = F.looped()

    for child in root:
      if child.tag == "digit":
        no, rect = find_no(child)
        _ = set_loop(), set_num(no)
        digit_rect[no] = rect

    assert is_loop(), "node has no child"
    cond, _ = is_valid()
    assert cond

    # return digit_rect, root, find_no, find_rect
    return digit_rect

  return read_xml_to_get(filename, func)


def get_single_digit_values(filename: P) -> t.Tuple[str, T.Rect]:
  """获取单个数字的值和位置信息

  Args:
      filename (P): XML文件路径

  Returns:
      Tuple[str, T.Rect]: 返回值和矩形框信息的元组
  """
  val, _ = read_xml_to_get(filename, read_rect_from_node)
  block_pos = read_xml_to_get(filename, read_single_digit_rect)
  return val, block_pos


def read_rect_from_file(xml_path: P, type_: typeOfrect):
  """从文件中读取矩形框信息

  Args:
      xml_path (P): XML文件路径
      type_ (typeOfrect): 矩形框类型，可以是'single'或'block'

  Returns:
      Any: 根据类型返回相应的矩形框信息
  """
  assert xml_path.suffix == ".xml"
  function_map: t.Mapping[typeOfrect, t.Callable[[P], t.Any]] = {
    "single": read_single_digit_rect,
    "block": get_rectangle,
  }
  func = function_map[type_]
  return func(xml_path)


def get_rectangle(filename: P) -> T.Rect:
  """获取矩形框信息

  Args:
      filename (P): XML文件路径

  Returns:
      T.Rect: 矩形框字典
  """
  _, rect = read_xml_to_get(filename, read_rect_from_node)
  return rect


def get_xml_config_path(
  img_path: P, types: t.Literal["value", "block", "single"] = "value"
) -> P:
  """根据图片路径获取对应的XML配置文件路径

  Args:
      img_path (P): 图片文件路径
      types (Literal): 配置类型，可以是'value'、'block'或'single'

  Returns:
      P: XML配置文件路径
  """
  dataset_path = img_path.parent

  def value_path():
    config_p = P(dataset_path) / "baocun"
    assert img_path.suffix in (".jpg", ".jpeg")
    filename = img_path.stem + ".xml"
    return config_p / filename

  def block_path():
    return P(dataset_path) / "config" / "block.xml"

  def single_path():
    return P(dataset_path) / "config" / "res.xml"

  funcs: t.Mapping[str, t.Callable] = {
    "value": value_path,
    "block": block_path,
    "single": single_path,
  }

  return funcs[types]()


def get_xml_config(img_path: P) -> t.Tuple[str, T.Rect]:
  """获取XML配置信息

  Args:
      img_path (P): 图片文件路径

  Returns:
      Tuple[str, T.Rect]: 返回值和矩形框信息的元组
  """
  return read_xml_to_get(
    filename=get_xml_config_path(img_path),
    read_func=read_rect_from_node,
  )
