import PyTeX.formatter
import PyTeX.base
import PyTeX.macros


class ClassFormatter(PyTeX.formatter.TexFormatter):
    def __init__(self, class_name: str, author: str, extra_header: [str] = []):
        PyTeX.formatter.TexFormatter.__init__(self, class_name, author, extra_header, '.cls')

    def make_default_macros(self):
        PyTeX.macros.make_default_macros(self, 'class')
