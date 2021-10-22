import git

from .git_version import get_latest_commit
from typing import Union, Optional, List


def is_recent(file, repo, compare: Optional[Union[git.Commit, List[git.Commit]]] = None) -> Optional[bool]:

    newly_committed_files = []
    if type(compare) == git.Commit:
        newly_committed_files = [item.a_path for item in repo.index.diff(compare)]
    elif type is None:
        newly_committed_files = [item.a_path for item in repo.index.diff(None)]
    elif type(compare) == list:
        for commit in compare:
            for item in repo.index.diff(commit):
                newly_committed_files.append(item.a_path)
    else:
        print("Invalid argument type for compare")
        return None

    if file in newly_committed_files:
        return True
    else:
        return False
