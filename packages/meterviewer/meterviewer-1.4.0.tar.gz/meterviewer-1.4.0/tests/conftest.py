import pytest
import pathlib
import typing as t
from pathlib import Path as P
from meterviewer.config import get_root_path


@pytest.fixture
def alldata() -> P:
  return P("alldata.db")


@pytest.fixture
def remove_files() -> t.Generator[t.Callable[[P], None], None, None]:
  filepath_list = []

  def func(filep: P):
    filepath_list.append(filep)

  yield func
  for filepath in filepath_list:
    filepath.unlink()


@pytest.fixture
def root_path() -> pathlib.Path:
  return get_root_path()
