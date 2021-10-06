from enums import Attributes, Args
from package_formatter import PackageFormatter


def make_default_commands(package_formatter: PackageFormatter):
    package_formatter.add_replacement('package name', '{}', Attributes.package_name)
    package_formatter.add_replacement('package prefix', '{}', Attributes.package_prefix)
    package_formatter.add_replacement('file name', '{name}', name=Attributes.file_name)
    package_formatter.add_replacement('header', '\\NeedsTeXFormat{{LaTeX2e}}\n'
                                                '\\ProvidesPackage{{{name}}}[{} - {}]\n'
                                                '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',
                                      Attributes.date,
                                      Attributes.description,
                                      name=Attributes.package_name)
    package_formatter.add_replacement('date', '{}', Attributes.date)
    package_formatter.add_replacement('author', '{}', Attributes.author)
    package_formatter.add_arg_replacement(1, 'newif', r'\newif\if{prefix}{condition}',
                                          prefix=Attributes.package_prefix, condition=Args.one)
    package_formatter.add_arg_replacement(2, 'setif', r'\{prefix}{condition}{value}',
                                          prefix=Attributes.package_prefix, condition=Args.one, value=Args.two)
    package_formatter.add_arg_replacement(1, 'if', r'\if{prefix}{condition}', prefix=Attributes.package_prefix,
                                          condition=Args.one)
    package_formatter.add_arg_replacement(1, 'info', r'\PackageInfo{{{name}}}{{{info}}}', name=Attributes.package_name,
                                          info=Args.one)
