from fabric.context_managers import cd
from profab.role import Role
from fabric.operations import sudo
from fabric.contrib.files import exists
from proteus import git_checkout, buildbot

def git_build_checkout(server, git_url, path):
    project_name = git_checkout.root_folder(git_url)
    git_folder = 'current/service'
    with cd(path):
        sudo("git clone -q %s %s" % (git_url, git_folder), user="www-data")
        # Point to develop branch
        with cd(git_folder):                       
            sudo("git checkout -b develop", user="www-data")
            sudo("git pull origin develop", user="www-data")
            sudo("git checkout develop", user="www-data")

class Configure(Role):
    """ 
    Checkout code from git_url to a path with parameters (path, git_url)
    """
    packages = ['git-core']
    def configure(self, server):
        git_url = self.parameter
        project_name = git_checkout.root_folder(git_url)
        buildbot.create_build_slave_layout(server, project_name)
        path = "/home/www-data/%s" % project_name
        git_build_checkout(server, git_url, path)

