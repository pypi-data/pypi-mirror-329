import abc


class Generator(abc.ABC):
  """所有生成器的入口，需要实现的生成函数"""

  @abc.abstractmethod
  def gen_func(self):
    pass


class Source(object):
  """"""

  pass


class ImageSource(Source):
  """原图像，定义清楚之后可以用于生成新的图像"""

  pass
