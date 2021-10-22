import git

from .git_version import get_latest_commit
from typing import Union, Optional, List
from pathlib import Path


def is_recent(file: Path, repo: git.Repo, compare: Optional[Union[git.Commit, List[git.Commit]]] = None) -> Optional[bool]:
    """
    :param file: file to check
    :param repo: repo that the file belongs to
    :param compare: commit or list of commits to compare to. None stands for 'working tree'
    :return: Whether the given file is currently the same as in compared commit

    If compare is a commit, checks if the file has changed since given commit, compared to the most recent commit
    of the repository
    For a list of commits, checks the same, but for all of these commits. In particular, only returns true if the file
    is the same in all of the specified commits (and in the most recent of the repository)

    If compare is None, compares the file against the corking tree, i.e. if the file has been modified since the last
    commit on the repo. This also involves staged files, i.e. modified and staged files will be considered as
    'not recent' since changes are not committed
    """
    newly_committed_files = []
    if type(compare) == git.Commit:
        newly_committed_files = [item.a_path for item in get_latest_commit(repo).diff(compare)]
    elif compare is None:
        com = get_latest_commit(repo)
        newly_committed_files = [item.a_path for item in com.diff(None)]
        pass
    elif type(compare) == list:
        for commit in compare:
            for item in get_latest_commit(repo).diff(commit):
                newly_committed_files.append(item.a_path)
    else:
        print("Invalid argument type for compare")
        return None

    if str(file.relative_to(repo.working_dir)) in newly_committed_files:
        return True
    else:
        return False
