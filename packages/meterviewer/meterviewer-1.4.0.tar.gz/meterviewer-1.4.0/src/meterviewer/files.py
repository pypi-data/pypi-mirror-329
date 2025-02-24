import pathlib
import typing as t
import numpy as np
from . import types as T
import hashlib

import toml


def use_smart_name(dataset: pathlib.Path) -> T.NameFunc:
  """
  Determine the appropriate file names for X and Y data in a dataset.
  Returns a function that provides the correct file names.
  """
  x_name_list = ["x_train.npy", "x_all.npy", "x.npy"]
  y_name_list = ["y_train.npy", "y_all.npy", "y.npy"]

  for x, y in zip(x_name_list, y_name_list):
    if (dataset / pathlib.Path(x)).exists() and (dataset / pathlib.Path(y)).exists():

      def get_x_y():
        return x, y

      return get_x_y
  else:
    raise Exception("No valid npy files found")


def compute_md5(file_path, chunk_size=8192):
  """
  Compute the MD5 hash of a file.

  Args:
      file_path (str): The path to the file.
      chunk_size (int): The size of each chunk to read from the file.

  Returns:
      str: The MD5 hash of the file in hexadecimal format.
  """
  md5_hash = hashlib.md5()

  with open(file_path, "rb") as f:
    while chunk := f.read(chunk_size):
      md5_hash.update(chunk)

  return md5_hash.hexdigest()


def read_toml(filename: pathlib.Path) -> t.Optional[t.Dict]:
  """
  Read and parse a TOML file, returning its contents as a dictionary.
  """
  try:
    with open(filename, "r") as f:
      data = toml.load(f)
      print(f"Read '{filename}' successfully.")
      return data
  except Exception as e:
    print(f"Error to read '{filename}': {e}")


def write_toml(filename: pathlib.Path, data):
  """
  Write data to a TOML file.
  """
  try:
    with open(filename, "w") as f:
      toml.dump(data, f)
    print(f"Data written to '{filename}' successfully.")
  except Exception as e:
    print(f"Error writing to '{filename}': {e}")


def write_shape(img: T.ImgList, nums: int = 3):
  """
  Write the shapes of the first 'nums' images to a debug log file.
  """
  debug_file = pathlib.Path("debug.log")
  with open(debug_file, "w") as f:
    for i in range(nums):
      f.write(f"img_{i} shape is: {img[i].shape}\n")


def scan_pics(path: pathlib.Path) -> t.Iterator[pathlib.Path]:
  """
  Scan a directory for image files (jpg, png, jpeg) and yield their paths.
  """
  for p in path.iterdir():
    if p.suffix in [".jpg", ".png", ".jpeg"]:
      yield p


def transform_img(img: T.NpImage) -> T.NpImage:
  """
  Reshape a single image by adding a batch dimension.
  """
  return np.expand_dims(img, axis=0)


def transform_label(label: T.DigitStr, to_int: bool) -> T.Label:
  """
  Transform a label string into a numpy array, optionally converting to integers.
  """
  if to_int:
    label_ = [int(i) for i in label]
  else:
    label_ = label
  return np.expand_dims(np.array(label_), axis=0)


def save_imgs_labels(
  imgs_labels: t.Tuple[t.List[T.NpImage], t.List[T.DigitStr]],
  np_name: t.Callable[[], t.Tuple[pathlib.Path, str, str]],
  save_to_disk: t.Callable,
):
  """
  Save a list of images and labels to disk as numpy arrays.
  """
  imgs, labels = imgs_labels
  imgs = [np.expand_dims(img, axis=0) for img in imgs]
  labels_ = [transform_label(label, False) for label in labels]
  x_train = np.vstack(imgs)
  y_train = np.vstack(labels_)

  prefix_path, x_name, y_name = np_name()
  save_to_disk(str(prefix_path / x_name), x_train)
  save_to_disk(str(prefix_path / y_name), y_train)


def save_img_labels_with_default(
  imgs: t.List[T.NpImage],
  labels: t.List[T.DigitStr],
  prefix_name: pathlib.Path,
  save_to_disk: t.Callable,
):
  """
  Save images and labels to disk using default file names.
  """

  def np_name():
    return prefix_name, T.x_name, T.y_name

  return save_imgs_labels(
    (imgs, labels),
    np_name,
    save_to_disk,
  )


def save_to_disk(filename: str, data: np.ndarray):
  """
  Save a numpy array to disk.
  """
  with open(filename, "wb") as f:
    np.save(f, data)


def load_from_disk(filename) -> np.ndarray:
  """
  Load a numpy array from disk.
  """
  with open(filename, "rb") as f:
    return np.load(f)


def load_from_disk_with_md5(filename, with_md5: str) -> t.Tuple[np.ndarray, str]:
  """
  Load a numpy array from disk and optionally compute its MD5 hash.
  """
  md5 = ""
  if with_md5:
    md5 = compute_md5(filename)
  return load_from_disk(filename), md5
