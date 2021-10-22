import git
import datetime
from typing import Optional, List

from PyTeX.build.git_hook import git_describe, get_latest_commit
from PyTeX.config.header_parts import *


class BuildInfo:
    def __init__(
            self,
            include_timestamp: bool = False,
            include_pytex_version: bool = False,
            include_license: bool = False,
            include_git_version: bool = False,
            include_pytex_info_text: bool = False,
            extra_header: Optional[List[str]] = None,
            author: Optional[str] = None,
            pytex_repo: Optional[git.Repo] = None,
            packages_repo: Optional[git.Repo] = None):

        self.author = author
        self.build_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')

        self._pytex_repo = pytex_repo
        self._packages_repo = packages_repo
        self._pytex_repo_commit = None
        self._packages_repo_commit = None
        self._pytex_repo_version = None
        self._packages_repo_version = None

        self._header = None

        self.get_repo_commits()
        self.get_repo_version()

        self.create_header(
            include_license=include_license,
            include_pytex_info_text=include_pytex_info_text,
            include_timestamp=include_timestamp,
            include_git_version=include_git_version,
            include_pytex_version=include_pytex_version,
            extra_header=extra_header
        )

    @property
    def header(self):
        return self._header

    @property
    def pytex_version(self):
        return self._pytex_repo_version

    @property
    def packages_version(self):
        return self._packages_repo_version

    @property
    def pytex_hash(self):
        return self._pytex_repo_commit.hexsha

    @property
    def packages_hash(self):
        return self._packages_repo_commit.hexsha

    @property
    def package_repo(self):
        return self._packages_repo

    @property
    def pytex_repo(self):
        return self._pytex_repo

    def get_repo_commits(self):
        if self._packages_repo:
            self._packages_repo_commit = get_latest_commit(self._packages_repo)
        if self._pytex_repo:
            self._pytex_repo_commit = get_latest_commit(self._pytex_repo)

    def get_repo_version(self):
        if self._packages_repo_commit:
            self._packages_repo_version = git_describe(self._packages_repo_commit)
        if self._pytex_repo_commit:
            self._pytex_repo_version = git_describe(self._pytex_repo_commit)

    def create_header(
            self,
            include_timestamp: bool = False,
            include_pytex_version: bool = False,
            include_license: bool = False,
            include_git_version: bool = False,
            include_pytex_info_text: bool = False,
            extra_header: Optional[List[str]] = None
    ):
        if not (include_license
                or include_pytex_info_text
                or include_timestamp
                or include_pytex_version
                or include_git_version):
            self._header = None
            return
        else:
            self._header = []
        if include_license:
            self._header += LICENSE + ['']
        if include_pytex_info_text:
            self._header += PYTEX_INFO_TEXT + ['']
        if include_timestamp or include_pytex_version or include_git_version:
            self._header += BUILD_DETAILS
        if include_timestamp:
            self._header += BUILD_TIME
        if include_pytex_version:
            self._header += PYTEX_VERSION
        if include_git_version:
            self._header += SOURCE_CODE_VERSION
        self._header += ['']
        if extra_header:
            self._header += extra_header + ['']

        if self._header[-1] == '':
            self._header.pop()

        formatted_header = []
        for line in self._header:
            formatted_header.append(line.format(
                year=datetime.datetime.now().strftime('%Y'),
                copyright_holders=self.author,
                source_file='{source_file}',
                latex_file_type='{latex_file_type}',
                pytex_version=self.pytex_version,
                pytex_commit_hash=self.pytex_hash[:7],
                packages_version=self.packages_version,
                packages_commit_hash=self.packages_hash[:7]
            ))
        self._header = formatted_header
