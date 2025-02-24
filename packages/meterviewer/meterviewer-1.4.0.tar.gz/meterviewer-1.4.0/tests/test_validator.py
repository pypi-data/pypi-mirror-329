from meterviewer.validator import check_if_meterdataset

dataset_path = "/data/xiu-hao/work/Dataset/MeterData/lens_6/XL/XL/M10L1XL"


def test_check_if_meterdataset():
  check_if_meterdataset(dataset_path)
