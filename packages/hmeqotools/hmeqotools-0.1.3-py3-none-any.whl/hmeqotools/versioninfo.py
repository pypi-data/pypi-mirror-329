"""版本信息"""

from __future__ import annotations
import datetime


class VersionInfo:
    def __init__(
        self,
        major=0,
        minor=0,
        micro=0,
        build=0,
        release: str = 'release',
        date: datetime.date | None = None,
    ):
        self.major = major
        self.minor = minor
        self.micro = micro
        self.build = build
        self.release = release
        self.date = date

    def __str__(self):
        return self.version

    @property
    def version(self):
        return f'{self.major}.{self.minor}.{self.micro}'

    @property
    def full_version(self):
        return f'{self.version}.{self.build}'

    @property
    def release_version(self):
        return f'{self.version} {self.release} {self.build}'


if __name__ == "__main__":
    version_info = VersionInfo(1, 1, 1, 0, "Release", datetime.date(2022, 3, 25))
    print(version_info.version)
