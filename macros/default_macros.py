import PyTeX.formatter
import PyTeX.base
import PyTeX.config


def make_default_macros(formatter: PyTeX.formatter.TexFormatter, latex_file_type: str):
    header = '\\NeedsTeXFormat{{LaTeX2e}}\n' \
             '\\Provides{Type}{{{name_lowercase}}}[{date} - {description}]\n\n'
    formatter.add_arg_replacement(
        1, 'header',
        header,
        name_lowercase=PyTeX.base.Attributes.name_lowercase,
        date=PyTeX.base.Attributes.date,
        description=PyTeX.base.Args.one,
        Type=latex_file_type.capitalize(),
    )
    formatter.add_replacement('{Type} name'.format(Type=latex_file_type), '{}', PyTeX.base.Attributes.name_lowercase)
    formatter.add_replacement('{Type} prefix'.format(Type=latex_file_type), '{}', PyTeX.base.Attributes.prefix)
    formatter.add_arg_replacement(1, '{Type} macro'.format(Type=latex_file_type), r'\{}{}',
                                  PyTeX.base.Attributes.prefix, PyTeX.base.Args.one)
    formatter.add_replacement('file name', '{name}', name=PyTeX.base.Attributes.file_name)
    formatter.add_replacement('date', '{}', PyTeX.base.Attributes.date)
    formatter.add_replacement('author', '{}', PyTeX.base.Attributes.author)
    formatter.add_arg_replacement(2, 'new if', r'\newif\if{prefix}{condition}\{prefix}{condition}{value}',
                                  prefix=PyTeX.base.Attributes.prefix, condition=PyTeX.base.Args.one,
                                  value=PyTeX.base.Args.two)
    formatter.add_arg_replacement(2, 'set if', r'\{prefix}{condition}{value}',
                                  prefix=PyTeX.base.Attributes.prefix, condition=PyTeX.base.Args.one,
                                  value=PyTeX.base.Args.two)
    formatter.add_arg_replacement(1, 'if', r'\if{prefix}{condition}', prefix=PyTeX.base.Attributes.prefix,
                                  condition=PyTeX.base.Args.one)
    formatter.add_replacement('language options x',
                              r'\newif\if{prefix}english\{prefix}englishtrue' + '\n' +
                              r'\DeclareOptionX{{german}}{{\{prefix}englishfalse}}' + '\n' +
                              r'\DeclareOptionX{{ngerman}}{{\{prefix}englishfalse}}' + '\n' +
                              r'\DeclareOptionX{{english}}{{\{prefix}englishtrue}}',
                              prefix=PyTeX.base.Attributes.prefix)
    formatter.add_replacement('language options',
                              r'\newif\if{prefix}english\{prefix}englishtrue' + '\n' +
                              r'\DeclareOption{{german}}{{\{prefix}englishfalse}}' + '\n' +
                              r'\DeclareOption{{ngerman}}{{\{prefix}englishfalse}}' + '\n' +
                              r'\DeclareOption{{english}}{{\{prefix}englishtrue}}',
                              prefix=PyTeX.base.Attributes.prefix)
    formatter.add_arg_replacement(1, 'info', r'\{Type}Info{{{name}}}{{{info}}}',
                                  name=PyTeX.base.Attributes.name_lowercase,
                                  info=PyTeX.base.Args.one, Type=latex_file_type.capitalize())
    formatter.add_arg_replacement(1, 'warning', r'\{Type}Warning{{{name}}}{{{warning}}}',
                                  name=PyTeX.base.Attributes.name_lowercase, warning=PyTeX.base.Args.one,
                                  Type=latex_file_type.capitalize())
    formatter.add_arg_replacement(1, 'error', r'\{Type}Error{{{name}}}{{{error}}}',
                                  name=PyTeX.base.Attributes.name_lowercase, error=PyTeX.base.Args.one,
                                  Type=latex_file_type.capitalize())
    formatter.add_replacement('end options x',
                              r"\DeclareOptionX*{{\{Type}Warning{{{name_lowercase}}}"
                              r"{{Unknown '\CurrentOption'}}}}" + '\n' + r'\ProcessOptionsX*\relax' + '\n',
                              name_lowercase=PyTeX.base.Attributes.name_lowercase, Type=latex_file_type.capitalize())
    formatter.add_replacement('end options',
                              r"\DeclareOption*{{\{Type}Warning{{{name_lowercase}}}"
                              r"{{Unknown '\CurrentOption'}}}}" + '\n' + r'\ProcessOptions\relax' + '\n',
                              name_lowercase=PyTeX.base.Attributes.name_lowercase, Type=latex_file_type.capitalize())
