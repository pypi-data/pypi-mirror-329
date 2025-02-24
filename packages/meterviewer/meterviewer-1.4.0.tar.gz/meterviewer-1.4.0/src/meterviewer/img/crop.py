import cv2
import numpy as np


def four_point_transform(image, pts):
  # 获取输入坐标点
  rect = np.float32(pts)

  # 计算输入的w和h值
  widthA = np.sqrt(((rect[2][0] - rect[3][0]) ** 2) + ((rect[2][1] - rect[3][1]) ** 2))
  widthB = np.sqrt(((rect[1][0] - rect[0][0]) ** 2) + ((rect[1][1] - rect[0][1]) ** 2))
  maxWidth = max(int(widthA), int(widthB))

  heightA = np.sqrt(((rect[1][0] - rect[2][0]) ** 2) + ((rect[1][1] - rect[2][1]) ** 2))
  heightB = np.sqrt(((rect[0][0] - rect[3][0]) ** 2) + ((rect[0][1] - rect[3][1]) ** 2))
  maxHeight = max(int(heightA), int(heightB))

  # 变换后的坐标
  dst = np.array(
    [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
    dtype="float32",
  )

  # 计算变换矩阵
  M = cv2.getPerspectiveTransform(rect, dst)

  # 执行变换
  warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

  return warped


def draw_points_and_lines(image, points):
  # 创建图片副本，避免修改原图
  img_copy = image.copy()

  # 绘制点
  for i, point in enumerate(points):
    x, y = map(int, point)
    # 画点（圆形），参数：图片，中心点，半径，颜色，粗细（-1表示填充）
    cv2.circle(img_copy, (x, y), 5, (0, 0, 255), -1)  # 红色点
    # 在点旁边添加序号
    cv2.putText(
      img_copy,
      str(i + 1),
      (x + 10, y + 10),
      cv2.FONT_HERSHEY_SIMPLEX,
      0.8,
      (0, 255, 0),
      2,
    )

  # 连接点（可选）
  # 连接成四边形
  for i in range(len(points)):
    pt1 = tuple(map(int, points[i]))
    pt2 = tuple(map(int, points[(i + 1) % len(points)]))
    cv2.line(img_copy, pt1, pt2, (255, 0, 0), 2)  # 蓝色线

  return img_copy
