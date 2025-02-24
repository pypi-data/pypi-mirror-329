from string import Template


def dataset():
  data = {}
  str_template = Template("$name_$peroid.npy")

  names = ["x", "y"]
  peroids = ["train", "test"]

  s = str_template.safe_substitute(name="train", peroid="2021")

  def get_root_path():
    pass
