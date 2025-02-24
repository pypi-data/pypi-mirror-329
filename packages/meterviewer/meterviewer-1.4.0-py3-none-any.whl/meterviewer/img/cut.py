# import cv2
from meterviewer import types as T


def cut_img(img: T.NpImage, rect: T.Rect) -> T.NpImage:
  cropped_image = img[rect.ymin : rect.ymax, rect.xmin : rect.xmax]
  return cropped_image
