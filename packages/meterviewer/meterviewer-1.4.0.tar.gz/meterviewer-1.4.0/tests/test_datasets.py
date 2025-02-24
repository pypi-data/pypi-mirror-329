from meterviewer import F
from meterviewer.datasets import dataset
from meterviewer.datasets.read import config


def test_read_single_digit(root_path):
  p = config.read_single_digit_rect(
    root_path / r"lens_6/XL/XL/M1L1XL" / "config" / "res.xml"
  )

  assert len(p) == 6
  p: list[config.RectO]
  assert p[0].xmax == "105", p[0]


def test_exist_dataset(root_path):
  assert dataset.get_dataset_path(root_path, r"M1L3XL").exists()


def test_read_xml(root_path):
  v, r = config.read_xml_to_get(
    root_path / r"lens_6/XL/XL/M1L3XL" / "baocun" / "2018-11-23-12-16-01.xml",
    config.read_rect_from_node,
  )
  assert v == "000994"
  assert r.get("xmin") == "79"


def test_img_to_xml(root_path):
  path_list = [
    config.get_xml_config_path(
      root_path / r"lens_6/XL/XL/M1L3XL" / "2018-11-23-12-16-01.jpg"
    ),
    config.get_xml_config_path(
      root_path / r"lens_6/XL/XL/M1L3XL" / "2018-11-23-12-16-01.jpg", "single"
    ),
  ]

  def path_exist(p):
    assert p.exists(), p

  F.must_loop(path_list, path_exist, custom_error=Exception)
