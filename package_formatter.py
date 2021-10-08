from formatter import Formatter
from config import DEFAULT_AUTHOR
from replacements import make_default_commands


class PackageFormatter(Formatter):
    def __init__(self, package_name: str, author: str = DEFAULT_AUTHOR, extra_header: str = ''):
        Formatter.__init__(self, package_name, author, extra_header, '.sty')

    def make_default_macros(self):
        make_default_commands(self, 'package')

