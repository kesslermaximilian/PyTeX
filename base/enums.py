from enum import Enum


class Attributes(Enum):
    name_raw = 'name_raw'
    author = 'author'
    author_acronym = 'author_acronym'
    name_lowercase = 'name_lowercase'
    prefix = 'prefix'
    file_name = 'file_name'
    date = 'date'
    year = 'year'
    source_file_name = 'source_file_name'


class Args(Enum):
    one = 0
    two = 1
    three = 2
    four = 3
    five = 4
