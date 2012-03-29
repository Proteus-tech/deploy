from profab.role import Role
from proteus.buildbot import virtual_env_path, home
from proteus.git_checkout import root_folder, git_checkout
from proteus.install_buildbot_slave_env import install_buildbot_slave_env
from proteus.setup_buildbot_slave import setup_buildbot_slave
from proteus.tag import tag

def slave_virtual_env_path(root):
    virtenv_path = virtual_env_path(root)
    return '%s-slave' % virtenv_path

def slave_location(root):
    return '%s/buildslave1' % (root)


class Configure(Role):
    """
    Add buildbot Slave with parameter "repository" 
    """
    packages = [ 'build-essential'
        , 'python-dev'
        , 'python-setuptools'
        , 'git-core'
    ]

    def configure(self, server):
        repository = self.parameter 
        project_name = root_folder(repository)
        root = home(project_name) 

        slave_virtenv = slave_virtual_env_path(root)
        install_buildbot_slave_env(server, slave_virtenv)
        tag(server, 'slave', 'env-installed')

        setup_buildbot_slave(server, root, 'slave1', 'localhost')

        slave_path = slave_location(root)
        slave_checkout_path = "%s/builder-sqlite" % (slave_path)
        git_checkout(server, slave_checkout_path, repository)
        tag(server, 'slave', 'ready')

