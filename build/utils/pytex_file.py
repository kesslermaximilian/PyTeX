from pathlib import Path
from typing import Optional

from PyTeX.build.git_hook import is_recent, get_latest_commit
from PyTeX import PackageFormatter, ClassFormatter
from .pytex_msg import pytex_msg

from .build_information import BuildInfo


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
            formatter = PackageFormatter(
                package_name=self.src_path.with_suffix('').name,
                author=self.current_build_info.author,
                extra_header=self.current_build_info.header)
        elif '.pycls' in self.src_path.name:
            formatter = ClassFormatter(
                class_name=self.src_path.with_suffix('').name,
                author=self.current_build_info.author,
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
