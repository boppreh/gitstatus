import os
import git

projects_dir = r'D:\projects'

class Repository(object):
    def __init__(self, name, repo):
        self.name = name
        self.repo = repo

    def __str__(self):
        status = 'Dirty' if self.repo.is_dirty() else 'Commited'
        sync = 'Out of sync' if not self.is_synced() else 'Synced'
        return '{} [{} {}]'.format(self.name, status, sync)

    def is_synced(self):
        remote = self.repo.remote()
        if not remote:
            return True

        local_commit = self.repo.commit()
        remote_commit = remote.fetch()[0].commit
        return local_commit.hexsha == remote_commit.hexsha


def get_repos():
    repos = []
    for folder in os.listdir(projects_dir):
        path = os.path.join(projects_dir, folder)
        try:
            repos.append(Repository(folder, git.Repo(path)))
        except git.exc.InvalidGitRepositoryError:
            continue
    return repos

for repo in get_repos():
    print repo
