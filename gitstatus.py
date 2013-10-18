import os
import git

projects_dir = r'D:\projects'
# Exclude private repos so we don't have to deal with authentication from
# fetches.
exclude = ['shamir', 'structured-editor']

class Repository(object):
    def __init__(self, name, repo):
        self.name = name
        self.repo = repo
        self.dirty_status = '?'
        self.sync_status = '?'

    def update_dirty_status(self):
        self.dirty_status = 'Dirty' if self.repo.is_dirty() else 'Commited'

    def update_sync_status(self):
        self.sync_status = 'Out of sync' if not self.is_synced() else 'Synced'

    def __str__(self):
        return '{} [{} {}]'.format(self.name, self.dirty_status,
                                   self.sync_status)

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
        if folder in exclude:
            continue

        path = os.path.join(projects_dir, folder)
        try:
            repos.append(Repository(folder, git.Repo(path)))
        except git.exc.InvalidGitRepositoryError:
            continue
    return repos
