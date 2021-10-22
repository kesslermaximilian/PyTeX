import json
from pathlib import Path
from typing import Optional

import git

import PyTeX

from .build_information import BuildInfo

from PyTeX.build.git_hook.recent import is_recent
from PyTeX.build.git_hook.git_version import get_latest_commit

BUILD_INFO_FILENAME = 'build_info.json'


def pytex_msg(msg: str):
    print('[PyTeX] ' + msg)


class TexFileToFormat:
    def __init__(
            self,
            src_path: Path,
            build_dir: Path,
            latex_name: str,
            current_build_info: BuildInfo,
            last_build_info: Optional[dict],
            allow_dirty: bool = False,
            overwrite_existing_files: bool = False,
            build_all: bool = False):
        self.src_path = src_path
        self.build_path = build_dir
        self.tex_name = latex_name  # Still an identifier on how to name the package when being formatted
        self.current_build_info = current_build_info
        self.last_build_info = last_build_info
        self.allow_dirty = allow_dirty
        self.overwrite_existing_files: overwrite_existing_files
        self.build_all = build_all

        self.dirty = not is_recent(self.src_path, self.current_build_info.package_repo, compare=None)
        self.pytex_dirty: bool = self.current_build_info.pytex_repo.is_dirty(
            working_tree=True,
            untracked_files=True
        )
        if self.last_build_info:
            self.recent: bool = is_recent(
                file=self.src_path,
                repo=self.current_build_info.package_repo,
                compare=self.current_build_info.package_repo.commit(self.last_build_info['source commit hash'])
            )
            self.pytex_recent: bool = get_latest_commit(
                self.current_build_info.pytex_repo
            ).hexsha == self.last_build_info['pytex commit hash']
        else:
            self.recent = False
            self.pytex_recent = False

    def format(self) -> dict:
        if self.dirty or self.pytex_dirty:
            if not self.allow_dirty:
                raise Exception(
                    '{file} is dirty, but writing dirty files not allowed.'.format(
                        file=self.src_path.name if self.dirty else 'Submodule PyTeX')
                )
            #  TODO: add this to the header...?
            return self.__format()  # Dirty files are always built, since we have no information about them
        elif self.build_all:
            return self.__format()  # Build file since we build all of them
        elif not self.pytex_recent or not self.recent:
            return self.__format()  # Build file since either pytex or package repo is not recent
        elif self.last_build_info and self.last_build_info['dirty']:
            return self.__format()  # Build file since we do not know in what state it is
        else:
            return self.last_build_info

    def __format(self) -> dict:
        if '.pysty' in self.src_path.name:
            formatter = PyTeX.PackageFormatter(
                package_name=self.src_path.with_suffix('').name,
                extra_header=self.current_build_info.header)
        elif '.pycls' in self.src_path.name:
            formatter = PyTeX.ClassFormatter(
                class_name=self.src_path.with_suffix('').name,
                extra_header=self.current_build_info.header)
        else:
            exit(1)
        pytex_msg('Writing file {}'.format(formatter.file_name))
        formatter.make_default_macros()
        formatter.format_file(self.src_path, self.build_path)
        info = {
            'name': formatter.file_name,
            'source file': self.src_path.name,
            'build time': self.current_build_info.build_time,
            'source version': self.current_build_info.packages_version,
            'source commit hash': self.current_build_info.packages_hash,
            'pytex version': self.current_build_info.pytex_version,
            'pytex commit hash': self.current_build_info.pytex_hash,
            'dirty': self.dirty
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
        use_git: bool = False,                        # versioning (not implemented yet)
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
        pytex_repo=git.Repo(__file__, search_parent_directories=True),
        packages_repo=git.Repo(src_dir, search_parent_directories=True)
    )
    input_dir = src_dir if src_dir else input_file.parent
    output_dir = build_dir if build_dir else input_file.parent

    last_build_info_file = output_dir / BUILD_INFO_FILENAME
    if last_build_info_file.exists():
        with open(output_dir / 'build_info.json', 'r') as f:
            last_build_info = json.load(f)
    else:
        last_build_info = None

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
        if last_build_info:
            last_build_info_for_this_file = next(
                (info for info in last_build_info['tex_sources'] if info['source file'] == file.name), {})
        else:
            last_build_info_for_this_file = None
        sources_to_build.append(
            TexFileToFormat(
                src_path=file,
                build_dir=output_dir / file.parent.relative_to(input_dir),
                latex_name=latex_name,
                current_build_info=current_build_info,
                last_build_info=last_build_info_for_this_file,
                allow_dirty=allow_dirty,
                overwrite_existing_files=overwrite_existing_files,
                build_all=build_all
            ))

    info_dict = {
        'build_time': '',
        'source files': {
            'version': current_build_info.packages_version,
            'commit': current_build_info.packages_hash,
            'dirty': current_build_info.package_repo.is_dirty(untracked_files=True)
        },
        'pytex': {
            'version': current_build_info.pytex_version,
            'commit': current_build_info.pytex_hash,
            'dirty': current_build_info.pytex_repo.is_dirty(untracked_files=True)
        },
        'tex_sources': [

        ]
    }

    for source in sources_to_build:
        info = source.format()
        info_dict['tex_sources'].append(info)

    if write_build_information:
        with open(output_dir / 'build_info.json', 'w') as f:
            json.dump(info_dict, f, indent=4)
    pytex_msg('Build done')
