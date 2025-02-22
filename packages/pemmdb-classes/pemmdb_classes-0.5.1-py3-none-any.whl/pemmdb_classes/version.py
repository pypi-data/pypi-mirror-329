#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christophe Druet"
__copyright__ = "Copyright (c) 2022-2024, ENTSO-E AISBL - All rights reserved"
__credits__ = ["Christophe Druet"]
__maintainer__ = "Christophe Druet"
__email__ = "christophe.druet@entsoe.eu"

from collections import namedtuple
from typing import List, Literal, Tuple


class Version(namedtuple('VersionBase', ['major', 'minor', 'patch'])):
    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


def parse(version_str: str) -> Version:
    return Version(*map(int, version_str.split(".")))


def _bump_version(version: Version, part: Literal["major", "minor", "patch"]):
    match part:
        case "major":
            return Version(major=version.major + 1, minor=0, patch=0)
        case "minor":
            return Version(major=version.major, minor=version.minor + 1, patch=0)
        case "patch":
            return Version(major=version.major, minor=version.minor, patch=version.patch + 1)
        case _:
            raise ValueError("Invalid part. Choose from 'major', 'minor', or 'patch'.")


# Generate a new version (e.g., based on date or bump)
def bump(current_version: str, 
         bump_type: Literal["major", "minor", "patch"] = "patch") -> str:
    """Bump the version based on type (major/minor/patch)."""
    version = parse(current_version)
    return str(_bump_version(version, bump_type))


def default() -> str:
    return '0.0.0'


def sort(version_strs: List[str]) -> List[str]:
    versions = [parse(v) for v in version_strs]
    versions.sort(key=lambda x: (x.major, x.minor, x.patch))
    return [str(v) for v in versions]


def get_latest(version_strs: List[str]) -> str:
    return sort(version_strs)[-1]


get_last = get_latest
