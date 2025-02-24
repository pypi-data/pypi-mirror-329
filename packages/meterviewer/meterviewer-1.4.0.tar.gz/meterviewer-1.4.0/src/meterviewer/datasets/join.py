"""用于单个仪表的拼接"""

import functools
import typing as t

from loguru import logger

from meterviewer import T
from meterviewer.img import process


def join_with_fix(
  imglist: T.ImgList,
  check_func: t.Callable,
  fix_func: t.Callable,
) -> T.NpImage:
  """修饰 join_func"""
  # merge images horizontally
  try:
    return process.join_img(imglist, check_func)
  except ValueError as e:
    logger.debug(e)
    imglist = fix_func(imglist)
  return process.join_img(imglist, check_func)


join_with_resize: T.JoinFunc = functools.partial(
  join_with_fix, fix_func=process.resize_imglist
)
