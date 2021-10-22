import PyTeX.formatter
import PyTeX.base
import PyTeX.macros


class PackageFormatter(PyTeX.formatter.TexFormatter):
    def __init__(self, package_name: str, author: str, extra_header: [str] = []):
        PyTeX.formatter.TexFormatter.__init__(self, package_name, author, extra_header, '.sty')

    def make_default_macros(self):
        PyTeX.macros.make_default_macros(self, 'package')
