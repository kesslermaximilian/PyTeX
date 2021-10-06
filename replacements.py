from enums import Attributes, Args
from package_formatter import PackageFormatter
from config import LICENSE, PACKAGE_INFO_TEXT


def make_default_commands(package_formatter: PackageFormatter):
    header = '%' * 80 + '\n' + '\n'.join(map(lambda line: '% ' + line, LICENSE + [''] + PACKAGE_INFO_TEXT)) \
             + '\n' + '%' * 80 + '\n' \
             + '\\NeedsTeXFormat{{LaTeX2e}}\n' \
               '\\ProvidesPackage{{{package_name}}}[{date} - {description}]\n\n'
    package_formatter.add_arg_replacement(
        1, 'header',
        header,
        package_name=Attributes.package_name,
        date=Attributes.date,
        description=Args.one,
        year=Attributes.year,
        copyright_holders=Attributes.author
    )
    package_formatter.add_replacement('package name', '{}', Attributes.package_name)
    package_formatter.add_replacement('package prefix', '{}', Attributes.package_prefix)
    package_formatter.add_arg_replacement(1, 'package macro', r'\{}{}', Attributes.package_prefix, Args.one)
    package_formatter.add_replacement('file name', '{name}', name=Attributes.file_name)
    package_formatter.add_replacement('date', '{}', Attributes.date)
    package_formatter.add_replacement('author', '{}', Attributes.author)
    package_formatter.add_arg_replacement(2, 'new if', r'\newif\if{prefix}{condition}\{prefix}{condition}{value}',
                                          prefix=Attributes.package_prefix, condition=Args.one, value=Args.two)
    package_formatter.add_arg_replacement(2, 'set if', r'\{prefix}{condition}{value}',
                                          prefix=Attributes.package_prefix, condition=Args.one, value=Args.two)
    package_formatter.add_arg_replacement(1, 'if', r'\if{prefix}{condition}', prefix=Attributes.package_prefix,
                                          condition=Args.one)
    package_formatter.add_replacement('language options',
                                      r'\newif\if{prefix}english\{prefix}englishtrue' + '\n' +
                                      r'\DeclareOptionX{{german}}{{\{prefix}englishfalse}}' + '\n' +
                                      r'\DeclareOptionX{{ngerman}}{{\{prefix}englishfalse}}' + '\n' +
                                      r'\DeclareOptionX{{english}}{{\{prefix}englishtrue}}',
                                      prefix=Attributes.package_prefix)
    package_formatter.add_arg_replacement(1, 'info', r'\PackageInfo{{{name}}}{{{info}}}', name=Attributes.package_name,
                                          info=Args.one)
    package_formatter.add_arg_replacement(1, 'warning', r'\PackageWarning{{{name}}}{{{warning}}}',
                                          name=Attributes.package_name, warning=Args.one)
    package_formatter.add_replacement('end options x',
                                      r"\DeclareOptionX*{{\PackageWarning{{{package_name}}}"
                                      r"{{Unknown '\CurrentOption'}}}}" + '\n' + r'\ProcessOptionsX\relax' + '\n',
                                      package_name=Attributes.package_name)
    package_formatter.add_replacement('end options',
                                      r"\DeclareOption*{{\PackageWarning{{{package_name}}}"
                                      r"{{Unknown '\CurrentOption'}}}}" + '\n' + r'\ProcessOptions\relax' + '\n',
                                      package_name=Attributes.package_name)
