from profab.role import Role
from proteus.buildbot import virtual_env_path, home, splitter
from proteus.git_checkout import root_folder, git_checkout
from proteus.install_buildbot_slave_env import install_buildbot_slave_env
from proteus.setup_buildbot_pg_slave import setup_buildbot_pg_slave
from proteus.tag import tag
from proteus.setup_library import setup_library
from proteus.buildbot_slave import slave_virtual_env_path, slave_location
from proteus.setup_psycopg2_on_slave import setup_psycopg2_on_slave

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
        try:
            repository, ec2_master_host = splitter(self.parameter)
        except ValueError:
            repository = self.parameter 
            ec2_master_host = 'localhost'

        # Derive project_name, root from repository.
        project_name = root_folder(repository)
        root = home(project_name) 

        # Setup buildbot-slave environment.
        slave_virtenv = slave_virtual_env_path(root)
        install_buildbot_slave_env(server, slave_virtenv)
        tag(server, 'slave', 'env-installed')

        # Setup buildbot-slave with postgres and create buildslave folder.
        setup_buildbot_pg_slave(server, root, 'slave-pg', ec2_master_host)

        # Checkout code from repository.
        slave_path = slave_location(root)
        slave_checkout_path = "%s/builder-pg" % (slave_path)
        git_checkout(server, slave_checkout_path, repository)
        setup_library(server, '%s/src/setup/requirelibs.txt' % (slave_checkout_path))

        # Setup python-psycopg2 in root environment and
        # psycopg2 in virtual environemt.
        setup_psycopg2_on_slave(server, slave_virtenv)

        tag(server, 'slave', 'ready')
