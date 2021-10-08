from formatter import Formatter
from config import DEFAULT_AUTHOR
from replacements import make_default_commands


class ClassFormatter(Formatter):
    def __init__(self, class_name: str, author: str = DEFAULT_AUTHOR, extra_header: str = ''):
        Formatter.__init__(self, class_name, author, extra_header, '.cls')

    def make_default_macros(self):
        make_default_commands(self, 'class')
