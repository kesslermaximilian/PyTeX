from enums import Attributes, Args
from formatter import Formatter
from config import LICENSE, PACKAGE_INFO_TEXT, PYTEX_INFO_TEXT


def make_default_commands(formatter: Formatter, latex_file_type: str):
    header = '%' * 80 + '\n' \
             + '\n'.join(map(lambda line: '% ' + line,
                             LICENSE + [''] + PACKAGE_INFO_TEXT + [''] + PYTEX_INFO_TEXT
                             + [''] + formatter.extra_header)
                         ) \
             + '\n' + '%' * 80 + '\n\n' \
             + '\\NeedsTeXFormat{{LaTeX2e}}\n' \
               '\\Provides{Type}{{{name_lowercase}}}[{date} - {description}]\n\n'
    formatter.add_arg_replacement(
        1, 'header',
        header,
        name_lowercase=Attributes.name_lowercase,
        date=Attributes.date,
        description=Args.one,
        year=Attributes.year,
        copyright_holders=Attributes.author,
        source_file=Attributes.source_file_name,
        Type=latex_file_type.capitalize(),
        latex_file_type=latex_file_type
    )
    formatter.add_replacement('{Type} name'.format(Type=latex_file_type), '{}', Attributes.name_lowercase)
    formatter.add_replacement('{Type} prefix'.format(Type=latex_file_type), '{}', Attributes.prefix)
    formatter.add_arg_replacement(1, '{Type} macro'.format(Type=latex_file_type), r'\{}{}', Attributes.prefix, Args.one)
    formatter.add_replacement('file name', '{name}', name=Attributes.file_name)
    formatter.add_replacement('date', '{}', Attributes.date)
    formatter.add_replacement('author', '{}', Attributes.author)
    formatter.add_arg_replacement(2, 'new if', r'\newif\if{prefix}{condition}\{prefix}{condition}{value}',
                                  prefix=Attributes.prefix, condition=Args.one, value=Args.two)
    formatter.add_arg_replacement(2, 'set if', r'\{prefix}{condition}{value}',
                                  prefix=Attributes.prefix, condition=Args.one, value=Args.two)
    formatter.add_arg_replacement(1, 'if', r'\if{prefix}{condition}', prefix=Attributes.prefix,
                                  condition=Args.one)
    formatter.add_replacement('language options x',
                                      r'\newif\if{prefix}english\{prefix}englishtrue' + '\n' +
                                      r'\DeclareOptionX{{german}}{{\{prefix}englishfalse}}' + '\n' +
                                      r'\DeclareOptionX{{ngerman}}{{\{prefix}englishfalse}}' + '\n' +
                                      r'\DeclareOptionX{{english}}{{\{prefix}englishtrue}}',
                              prefix=Attributes.prefix)
    formatter.add_replacement('language options',
                                      r'\newif\if{prefix}english\{prefix}englishtrue' + '\n' +
                                      r'\DeclareOption{{german}}{{\{prefix}englishfalse}}' + '\n' +
                                      r'\DeclareOption{{ngerman}}{{\{prefix}englishfalse}}' + '\n' +
                                      r'\DeclareOption{{english}}{{\{prefix}englishtrue}}',
                              prefix=Attributes.prefix)
    formatter.add_arg_replacement(1, 'info', r'\{Type}Info{{{name}}}{{{info}}}', name=Attributes.name_lowercase,
                                  info=Args.one, Type=latex_file_type.capitalize())
    formatter.add_arg_replacement(1, 'warning', r'\{Type}Warning{{{name}}}{{{warning}}}',
                                  name=Attributes.name_lowercase, warning=Args.one, Type=latex_file_type.capitalize())
    formatter.add_arg_replacement(1, 'error', r'\{Type}Error{{{name}}}{{{error}}}',
                                  name=Attributes.name_lowercase, error=Args.one, Type=latex_file_type.capitalize())
    formatter.add_replacement('end options x',
                                      r"\DeclareOptionX*{{\{Type}Warning{{{name_lowercase}}}"
                                      r"{{Unknown '\CurrentOption'}}}}" + '\n' + r'\ProcessOptionsX\relax' + '\n',
                              name_lowercase=Attributes.name_lowercase, Type=latex_file_type.capitalize())
    formatter.add_replacement('end options',
                                      r"\DeclareOption*{{\{Type}Warning{{{name_lowercase}}}"
                                      r"{{Unknown '\CurrentOption'}}}}" + '\n' + r'\ProcessOptions\relax' + '\n',
                              name_lowercase=Attributes.name_lowercase, Type=latex_file_type.capitalize())
