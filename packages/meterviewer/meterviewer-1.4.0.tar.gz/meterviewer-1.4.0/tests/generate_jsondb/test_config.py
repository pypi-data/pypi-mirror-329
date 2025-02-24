from meterviewer.generator.jsondb import get_dataset


def test_get_all_dataset(set_config):
  assert len(get_dataset(5, True).dataset_list) > 0
