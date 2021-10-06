from enum import Enum


class Attributes(Enum):
    package_name_raw = 'package_name_raw'
    author = 'author'
    author_acronym = 'author_acronym'
    package_name = 'package_name'
    package_prefix = 'package_prefix'
    file_name = 'file_name'
    date = 'date'
    year = 'year'


class Args(Enum):
    one = 0
    two = 1
    three = 2
    four = 3
    five = 4
