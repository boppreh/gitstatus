import os
import git

projects_dir = r'D:\projects'

class Repository(object):
    def __init__(self, name, repo):
        self.name = name
        self.repo = repo

    def __str__(self):
        return self.name


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
