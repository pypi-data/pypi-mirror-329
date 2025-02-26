from __future__ import annotations

import os
import sys


def is_writable(path: str):
    """Test if the path is writable."""
    try:
        os.chmod(path, os.stat(path).st_mode)
    except OSError:
        return False
    return True


def get_profile_path() -> str:
    return os.path.expanduser("~")


def get_desktop_path() -> str:
    return os.path.expanduser("~/Desktop")


if sys.platform == "win32":

    def get_mounts() -> list[str]:
        """Get the mount points (currently only supported on Windows)."""
        result = []
        for name in os.popen("wmic logicaldisk get Name"):
            name = name.strip()
            if name and not name.endswith(os.sep) and os.path.exists(name):
                result.append(name)
        return result


def main():
    print(get_desktop_path())


if __name__ == "__main__":
    main()
