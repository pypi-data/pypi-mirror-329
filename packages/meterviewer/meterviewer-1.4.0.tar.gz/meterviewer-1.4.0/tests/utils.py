import numpy as np
from matplotlib import pyplot as plt


def visualize_check(img, title):
  # 显示一个带确认按钮的窗口，如果确认则返回True，否则返回False
  pass


def show_img(img):
  # TODO: img valid test. use a gui to validate.
  is_show = 1
  if is_show:
    plt.imshow(img)
    plt.show()


def gen_img(size=(35, 25, 3)):
  return np.random.randint(0, 255, size=size, dtype=np.uint8)
