import datetime
import re
from pathlib import Path
from typing import Dict
from datetime import *
from config import DEFAULT_AUTHOR
from enums import Attributes, Args


class PackageFormatter:
    def __init__(self, package_name: str, author: str = DEFAULT_AUTHOR):
        self.package_name_raw = package_name
        self.author = author
        author_parts = self.author.lower().replace('ß', 'ss').split(' ')
        self.author_acronym = author_parts[0][0] + author_parts[-1]
        self.package_name = r'{prefix}-{name}'.format(prefix=self.author_acronym,
                                                      name=self.package_name_raw.lower().strip().replace(' ', '-'))
        self.package_prefix = self.package_name.replace('-', '@') + '@'
        self.file_name = self.package_name + '.sty'
        self.date = datetime.now().strftime('%Y/%m/%d')
        self.year = int(datetime.now().strftime('%Y'))
        self.replace_dict: Dict = {}
        self.arg_replace_dict: Dict = {}

    @staticmethod
    def command_name2keyword(keyword: str):
        return '__' + keyword.upper().strip().replace(' ', '_') + '__'

    def parse_replacement_args(self, match_groups, *user_args, **user_kwargs):
        new_args = []
        for arg in user_args:
            if type(arg) == Attributes:
                new_args.append(getattr(self, arg.value))
            elif type(arg) == Args:
                new_args.append(match_groups[arg.value])
            elif type(arg) == str:
                new_args.append(arg)
            else:
                new_args += 'ERROR'
        new_args = tuple(new_args)
        new_kwargs = {}
        for kw in user_kwargs:
            if type(user_kwargs[kw]) == Attributes:
                new_kwargs[kw] = getattr(self, user_kwargs[kw].value)
            elif type(user_kwargs[kw]) == Args:
                new_kwargs[kw] = match_groups[user_kwargs[kw].value]
            elif type(user_kwargs[kw]) == str:
                new_kwargs[kw] = user_kwargs[kw]
            else:
                new_kwargs[kw] = 'ERROR'
        return new_args, new_kwargs

    def add_replacement(self, keyword: str, replacement: str, *args, **kwargs):
        args, kwargs = self.parse_replacement_args([], *args, **kwargs)
        self.replace_dict[self.command_name2keyword(keyword)] = replacement.format(*args, **kwargs)

    def add_arg_replacement(self, num_args: int, keyword: str, replacement: str, *args, **kwargs):
        self.arg_replace_dict[self.command_name2keyword(keyword)] = {
            'num_args': num_args,
            'replacement': replacement,
            'format_args': args,
            'format_kwargs': kwargs
        }

    def format(self, contents: str) -> str:
        for key in self.replace_dict.keys():
            contents = contents.replace(key, self.replace_dict[key])
        return contents

    def format_with_arg(self, contents: str) -> str:
        for command in self.arg_replace_dict.keys():
            search_regex = re.compile(r'{keyword}\({arguments}(?<!@)\)'.format(
                keyword=command,
                arguments=','.join(['(.*?)'] * self.arg_replace_dict[command]['num_args'])
            ))
            match = re.search(search_regex, contents)
            while match is not None:
                format_args, format_kwargs = self.parse_replacement_args(
                    list(map(lambda group: group.replace('@)', ')'), match.groups())),
                    *self.arg_replace_dict[command]['format_args'],
                    **self.arg_replace_dict[command]['format_kwargs']
                )
                contents = contents.replace(
                    match.group(),
                    self.arg_replace_dict[command]['replacement'].format(*format_args, **format_kwargs)
                )
                match = re.search(search_regex, contents)
        return contents

    def format_package(self, input_path: Path, output_dir: Path = None):
        input_file = input_path.open()
        lines = input_file.readlines()
        newlines = []
        for line in lines:
            newlines += self.format_with_arg(self.format(line))
        if output_dir is None:
            output_dir = input_path.parent
        (output_dir / self.file_name).write_text(''.join(newlines))
