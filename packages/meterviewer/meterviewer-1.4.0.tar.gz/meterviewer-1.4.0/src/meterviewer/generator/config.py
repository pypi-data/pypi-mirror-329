import typing as t


class BasicConfig(t.TypedDict):
  name: str
  size: int


# try define a object as js way
base_config: BasicConfig = {
  "name": "empty",
  "size": 10,
}
