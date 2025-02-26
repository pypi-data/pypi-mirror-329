from __future__ import annotations

import ctypes
import sys
from os import PathLike


def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except WindowsError:
        return False


def runas(fp: str | PathLike[str]) -> int:
    """以管理员身份运行.
    返回42为成功, 5为失败
    """
    return ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, fp, None, 1)
