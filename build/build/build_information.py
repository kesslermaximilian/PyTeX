import git
import datetime
from typing import Optional

from PyTeX.build.git_hook import git_describe, get_latest_commit

from .config import BUILD_DETAILS


def build_information():
    repo = git.Repo()
    repo_description = git_describe(get_latest_commit(repo))
    pytex_repo = repo.submodule('PyTeX').module()
    pytex_repo_description = git_describe(get_latest_commit(pytex_repo))
    return list(map(lambda line: line.format(
        build_time=datetime.datetime.now().strftime('%Y/%m/%d %H:%M'),
        pytex_version=pytex_repo_description,
        pytex_commit_hash=get_latest_commit(pytex_repo).hexsha[0:7],
        packages_version=repo_description,
        packages_commit_hash=get_latest_commit(repo).hexsha[0:7]
    ), BUILD_DETAILS)), repo_description


class BuildInfo:
    def __init__(
            self,
            include_timestamp: bool = False,
            include_pytex_version: bool = False,
            include_license: bool = False,
            include_git_version: bool = False,
            include_pytex_info_text: bool = False,
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
            include_timestamp=include_timestamp,
            include_pytex_version=include_pytex_version,
            include_license=include_license,
            include_git_version=include_git_version,
            include_pytex_info_text=include_pytex_info_text
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
            include_pytex_info_text: bool = False):
        self._header = []
