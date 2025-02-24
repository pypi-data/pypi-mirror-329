from pydantic import BaseModel


class Item(BaseModel):
  filepath: str
  dataset: str

  xmin: float
  xmax: float
  ymin: float
  ymax: float


class MeterDB(BaseModel):
  """the data load from the meterdb.json"""

  data: list[Item]
