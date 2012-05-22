from fabric.context_managers import cd
from profab.role import Role
from fabric.operations import sudo
from fabric.contrib.files import exists
from proteus import git_checkout

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

def create_build_slave_layout(server, project_name):
    base_folder = '/home/www-data'
    with cd(base_folder):
        current_folder = '%s/current' % (project_name)
        config_folder = '%s/config' % (project_name)
        logs_folder = '%s/logs' % (project_name)
        bin_folder = '%s/bin' % (project_name)

        sudo('mkdir -p %s' % (current_folder), user="www-data") 
        sudo('mkdir -p %s' % (config_folder), user="www-data")
        sudo('mkdir -p %s' % (logs_folder), user="www-data")
        sudo('mkdir -p %s' % (bin_folder), user="www-data")

        sudo('mkdir -p %s/service' % (current_folder), user="www-data")
        sudo('mkdir -p %s/virtualenv' % (current_folder), user="www-data")
        sudo('mkdir -p %s/static' % (current_folder), user="www-data")

        buildbot_folder = '%s/buildbot' % (project_name)
        sudo('mkdir -p %s' % (buildbot_folder), user="www-data")
        sudo('mkdir -p %s/master' % (buildbot_folder), user="www-data")
        sudo('mkdir -p %s/slave1' % (buildbot_folder), user="www-data")

class Configure(Role):
    """ 
    Checkout code from git_url to a path with parameters (path, git_url)
    """
    packages = ['git-core']
    def configure(self, server):
        git_url = self.parameter
        project_name = git_checkout.root_folder(git_url)
        create_build_slave_layout(server, project_name)
        path = "/home/www-data/%s" % project_name
        git_build_checkout(server, git_url, path)

