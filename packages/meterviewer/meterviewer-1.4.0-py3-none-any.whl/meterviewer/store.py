data = {}


def useDict(name):
  data[name] = []

  def insert(item):
    data[name].append(item)

  return insert
