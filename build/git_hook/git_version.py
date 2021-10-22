import git
from typing import Dict


def get_latest_commit(repo):
    if repo.head.is_detached:
        return repo.head.commit
    else:
        return repo.head.ref.commit


def get_history(commit: git.objects.commit.Commit, priority=0, depth=0) -> Dict:
    commit_history = {commit.hexsha: {
        'priority': priority,
        'depth': depth
    }}
    try:
        if len(commit.parents) > 0:
            commit_history.update(get_history(commit.parents[0], priority, depth + 1))
            for parent in commit.parents[1:]:
                commit_history.update(get_history(parent, priority + 1, depth + 1))
    except ValueError:
        pass
    return commit_history


def git_describe(commit: git.objects.commit.Commit):
    commit_history = get_history(commit)
    latest_tag = None
    for tag in commit.repo.tags:
        sha = tag.commit.hexsha
        if sha in commit_history.keys():
            if latest_tag is None:
                latest_tag = tag
            elif commit_history[sha]['priority'] < commit_history[latest_tag.commit.hexsha]['priority']:
                latest_tag = tag
            elif commit_history[sha]['priority'] > commit_history[latest_tag.commit.hexsha]['priority']:
                pass  # move on
            elif commit_history[sha]['depth'] < commit_history[latest_tag.commit.hexsha]['depth']:
                latest_tag = tag
            elif commit_history[sha]['depth'] > commit_history[latest_tag.commit.hexsha]['depth']:
                pass  # move on
            elif tag.object.tagged_date > latest_tag.object.tagged_date:
                latest_tag = tag
    if latest_tag is None:
        return "No tags found - cannot describe anything."
    else:
        msg = latest_tag.name
        if commit_history[latest_tag.commit.hexsha]['depth'] != 0:
            msg += "-{depth}".format(depth=commit_history[latest_tag.commit.hexsha]['depth'])
        if commit.repo.is_dirty(untracked_files=True):
            msg += '-*'
        return msg
