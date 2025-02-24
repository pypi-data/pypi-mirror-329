from pathlib import Path as P


def check_if_meterdataset(path: P) -> bool:
  """
  Check if the dataset is meter-formatted.

  """

  must_exist_folder = [
    "baocun",
    "config",
    "coor_all_img_np",
    "Digit",
    "id",
    "ImageSets",
    "ImageSets_block_zoom",
    "ImageSets_seg",
    "Numpy_block_zoom",
    "Numpy_seg",
  ]

  must_exist_folder = [P(folder) for folder in must_exist_folder]

  for folder in must_exist_folder:
    if not (path / folder).exists():
      raise ValueError(f"Folder {folder} does not exist in {path}")
