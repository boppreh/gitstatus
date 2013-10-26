import threading
import time
import os
from subprocess import check_output

projects_dir = r'D:\projects'

class Repository(object):
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.dirty_status = '?'
        self.sync_status = '?'

    def update_dirty_status(self):
        if len(self.git('status --porcelain')):
            self.dirty_status = 'Dirty'
        else:
            self.dirty_status = 'Commited'

    def update_sync_status(self):
        self.git('fetch', true) 
        output = self.git('status --porcelain').decode('utf-8')
        if 'Your branch is behind' in output or 'Your branch is ahead' in output:
            self.sync_status = 'Out of sync'
        else:
            self.sync_status = 'Synced'

    def __str__(self):
        return '{} [{} {}]'.format(self.name, self.dirty_status,
                                   self.sync_status)

    def git(self, command, ignore_output=False):
        template = 'git --git-dir="{}" --work-tree="{}" {}'
        command = template.format(os.path.join(self.path, '.git'), self.path,
                                  command)
        if ignore_output:
            return os.system(command)
        else:
            return check_output(command)

def get_repos():
    for folder in os.listdir(projects_dir):
        path = os.path.join(projects_dir, folder)
        if os.path.exists(os.path.join(path, '.git')):
            yield Repository(folder, path)

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
    repos = list(get_repos())

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
    serve(lambda: map(str, repos), port=2347)
