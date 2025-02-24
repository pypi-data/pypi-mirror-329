import cv2

from meterviewer import types as T


# draw rectangle on image
def draw_rectangle(im: T.NpImage, rect: T.Rect) -> T.NpImage:
  """draw rectangle on image"""
  x0, y0, x1, y1 = rect.xmin, rect.ymin, rect.xmax, rect.ymax
  writable_im = im.copy()
  cv2.rectangle(writable_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
  return writable_im


# write text on image
def draw_text(
  im: T.NpImage,
  text: str,
) -> T.NpImage:
  """write text on image"""
  x, y = 0, 30
  writable_im = im.copy()
  cv2.putText(writable_im, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
  return writable_im
