import pathlib
import platform
import typing as t


def get_root_path():
  def get_system_type() -> t.Literal["macOS", "Windows", "Other", "Linux"]:
    """
    判断当前系统类型是 macOS 还是 Windows。

    Returns:
        str: 'macOS', 'Windows' 或 'Other'，分别表示 macOS 系统、Windows 系统或其他系统。
    """
    system = platform.system()

    if system == "Darwin":
      return "macOS"
    elif system == "Windows":
      return "Windows"
    elif system == "Linux":
      return "Linux"
    else:
      return "Other"

  if get_system_type() == "macOS":
    # expand userhome
    return pathlib.Path("/Volumes/Fast SSD/Research/Dataset/MeterData")
  elif get_system_type() == "Windows":
    return pathlib.Path(r"D:\Store\MeterData")
  elif get_system_type() == "Linux":
    return pathlib.Path("~/Work/Dataset/MeterData").expanduser()
  else:
    raise Exception("Not work under Linux now. 2024-05-21.")
