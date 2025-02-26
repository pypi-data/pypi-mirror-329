"""Find and delete pycache directory."""

import os
import shutil
from collections import deque

cache_dirnames = ["__pycache__", ".pdm-build"]


def main():
    path_list = deque(["."])
    while path_list:
        for i in os.scandir(path_list.popleft()):
            if not i.is_dir():
                continue
            if i.name in cache_dirnames:
                shutil.rmtree(i.path)
            else:
                path_list.append(i.path)


if __name__ == "__main__":
    main()
