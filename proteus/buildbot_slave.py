from profab.role import Role
from proteus.buildbot import virtual_env_path 
from proteus.git_checkout import root_folder, git_checkout
from proteus.install_buildbot_slave_env import install_buildbot_slave_env
from proteus.setup_buildbot_slave import setup_buildbot_slave
from proteus.tag import tag

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
        root = "/home/www-data/Buildbot/%s" % (project_name)

        virtenv_path = virtual_env_path(root)
        slave_virtenv = '%s-slave' % virtenv_path
        install_buildbot_slave_env(server, slave_virtenv)
        tag(server, 'slave', 'env-installed')

        setup_buildbot_slave(server, root, 'slave1', 'localhost')

        slave_path = '%s/buildslave1' % (root)
        slave_checkout_path = "%s/builder-sqlite" % (slave_path)
        git_checkout(server, slave_checkout_path, repository)
        tag(server, 'slave', 'ready')

