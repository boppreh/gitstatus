import threading
import time
import os
import git

projects_dir = r'D:\projects'
exclude = ['old']

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

class Updater(threading.Thread):
    def __init__(self, interval, function):
        threading.Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.cancelled = False

    def run(self):
        while not self.cancelled:
            time.sleep(self.interval)
            self.function()

if __name__ == '__main__':
    repos = get_repos()

    def update_dirty_status():
        for repo in repos:
            repo.update_dirty_status()

    def update_sync_status():
        for repo in repos:
            repo.update_sync_status()

    Updater(60, update_dirty_status).start()
    Updater(60 * 30, update_sync_status).start()

    from tray import tray
    tray('Git Status', 'git.png')

    from simpleserver import serve
    serve(lambda: map(str, repos), port=4327)
