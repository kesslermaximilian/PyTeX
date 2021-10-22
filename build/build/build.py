import json
from pathlib import Path
from typing import Optional

import git

import PyTeX

from .build_information import BuildInfo


def pytex_msg(msg: str):
    print('[PyTeX] ' + msg)


class TexFileToFormat:
    def __init__(self, src_path: Path, build_dir: Path, latex_name: str, build_info: BuildInfo):
        self.src_path = src_path
        self.build_path = build_dir
        self.tex_name = latex_name  # Still an identifier on how to name the package when being formatted
        self.build_info = build_info

    def format(self):
        if '.pysty' in self.src_path.name:
            formatter = PyTeX.PackageFormatter(
                package_name=self.src_path.with_suffix('').name,
                extra_header=self.build_info.header)
        else:
            formatter = PyTeX.ClassFormatter(
                class_name=self.src_path.with_suffix('').name,
                extra_header=self.build_info.header)
        pytex_msg('Writing file {}'.format(formatter.file_name))
        formatter.make_default_macros()
        formatter.format_file(self.src_path, self.build_path)
        info = {
            'name': formatter.file_name,
            'source file': self.src_path.name,
            'build time': self.build_info.build_time,
            'source version': self.build_info.packages_version,
            'source commit hash': self.build_info.packages_hash,
            'pytex version': self.build_info.pytex_version,
            'pytex commit hash': self.build_info.pytex_hash,
            'dirty': False
        }
        return info


def build(
        src_dir: Optional[Path] = None,
        build_dir: Optional[Path] = None,
        input_file: Optional[Path] = None,
        author: Optional[str] = None,
        latex_name: str = 'prepend-author',           # name handling
        recursive: bool = False,                      # input control
        include_timestamp: bool = False,              # header
        include_pytex_version: bool = False,          # header
        include_license: bool = False,                # header
        include_git_version: bool = False,            # header
        include_pytex_info_text: bool = False,        # header
        use_git: bool = False,                        # versioning
        allow_dirty: bool = False,                    # versioning
        overwrite_existing_files: bool = False,       # output control
        build_all: bool = False,                      # output control / versioning
        write_build_information: bool = True,         # meta
        ):
    pytex_msg('Getting git repository information...')
    current_build_info = BuildInfo(
        include_timestamp=include_timestamp,
        include_pytex_version=include_pytex_version,
        include_license=include_license,
        include_git_version=include_git_version,
        include_pytex_info_text=include_pytex_info_text,
        author=author,
        pytex_repo=git.Repo(__file__, search_parent_directories=True),  # TODO
        packages_repo=git.Repo(src_dir, search_parent_directories=True)  # TODO
    )
    input_dir = src_dir if src_dir else input_file.parent
    output_dir = build_dir if build_dir else input_file.parent

    with open(output_dir / 'build_info.json') as f:
        old_build_info = json.load(f)
    # extra_header += ['WARNING: Local changes to git repository detected.',
    #                     '         The build will not be reproducible (!)']

    files = []
    if input_file:
        files.append(input_file)
    if src_dir:
        if recursive:
            for file in src_dir.rglob('*.pysty'):
                files.append(file)
            for file in src_dir.rglob('*.pycls'):
                files.append(file)
        else:
            for file in src_dir.glob('*.pysty'):
                files.append(file)
            for file in src_dir.glob('*.pycls'):
                files.append(file)

    sources_to_build = []
    for file in files:
        sources_to_build.append(
            TexFileToFormat(
                src_path=file,
                build_dir=output_dir / file.parent.relative_to(input_dir),
                latex_name=latex_name,
                build_info=current_build_info
            ))

    info_dict = {
        'build_time': '',
        'LatexPackages': {
            'version': current_build_info.packages_version,
            'commit': current_build_info.packages_hash,
            'dirty': False  # TODO
        },
        'PyTeX': {
            'version': current_build_info.pytex_version,
            'commit': current_build_info.pytex_hash,
            'dirty': False  # TODO
        },
        'tex_sources': [

        ]
    }

    for source in sources_to_build:
        info = source.format()
        info_dict['tex_sources'].append(info)
    with open(output_dir / 'build_info.json', 'w') as f:
        json.dump(info_dict, f, indent=4)
    pytex_msg('Build done')
