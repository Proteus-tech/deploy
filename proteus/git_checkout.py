from fabric.context_managers import cd
from fabric.operations import sudo
from profab.role import Role
from proteus import buildbot

def root_folder(git_url):
    git_folder = git_url.split('/')[-1]
    return git_folder.split('.git')[0]

def git_checkout(server, path, git_url):
    with cd(path):
        git_folder = 'src'
        sudo("git clone -q %s %s" % (git_url, git_folder), user="www-data")
        # Point to develop branch
        with cd(git_folder):                   
            sudo("git checkout -b develop", user="www-data")
            sudo("git pull origin develop", user="www-data")
            sudo("git checkout develop", user="www-data")


class Configure(Role):
    """
    Checkout code from git_url to a path with parameters (git_url, path)
    """
    packages = ['git-core']

    def configure(self, server):
        path, git_url = buildbot.splitter(self.parameter)
        git_checkout(server, path, git_url)

