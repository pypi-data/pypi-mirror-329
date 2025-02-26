from __future__ import annotations

import os
import winreg


class Key:
    def __init__(self, key: int, sub_key: str) -> None:
        self.key = key
        self.sub_key = sub_key

    def open(self, reserved: int = 0, access: int = winreg.KEY_READ):
        return winreg.OpenKey(self.key, self.sub_key, reserved, access)


class HKEY_CLASSES_ROOT:

    HKEY = winreg.HKEY_CLASSES_ROOT
    FILE_MENU = Key(HKEY, r"*\shell")


class HKEY_LOCAL_MACHINE:

    HKEY = winreg.HKEY_LOCAL_MACHINE
    DRIVERS = Key(HKEY, r"SYSTEM\MountedDevices")
    ENVIRONMENT = Key(HKEY, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
    RUN = Key(HKEY, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")


class HKEY_CURRENT_USER(Key):

    HKEY = winreg.HKEY_CURRENT_USER
    SHELL_FOLDER = Key(HKEY, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
    RUN = Key(HKEY, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")


def get_drives():
    """Get the list of available drives."""
    drives = []
    key = HKEY_LOCAL_MACHINE.DRIVERS.open()
    prefix = "\\DosDevices\\"
    index = 0
    try:
        while True:
            name = winreg.EnumValue(key, index)[0]
            if name.startswith(prefix):
                mount = name[len(prefix):] + os.sep
                if os.path.exists(mount):
                    drives.append(mount)
            index += 1
    except WindowsError as exc:
        if exc.winerror != 259:
            raise exc
    return drives


def get_desktop_path():
    """Get desktop path."""
    key = HKEY_CURRENT_USER.SHELL_FOLDER.open()
    return winreg.QueryValueEx(key, "Desktop")[0]
