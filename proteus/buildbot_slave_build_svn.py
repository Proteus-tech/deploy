#!/usr/bin/env python
from fabric.context_managers import cd, prefix
from fabric.operations import sudo

from profab.role import Role
from proteus.buildbot import virtual_env_path, home, splitter
from proteus.svn_checkout import root_folder, svn_checkout
from proteus.install_buildbot_slave_env import install_buildbot_slave_env
from proteus.setup_buildbot_slave import setup_buildbot_slave
from proteus.tag import tag

def slave_build_virtual_env_path(root):
    virtenv_path = virtual_env_path(root)
    return '%s-slave-build' % virtenv_path

def slave_build_location(root):
    return '%s/buildslave1-build' % (root)

#def setup_buildbot_slave_build(slave, root, name, master_host):
#    virtenv_path = '%s-slave-build' % virtual_env_path(root)
#    base_dir = 'buildslave1-build'
#    password = '%spassword' % name
#    parameters = "%s %s %s %s" % (base_dir, master_host, name, password)
#    with prefix("source %s/bin/activate" % (virtenv_path)):
#        with cd(root):
#            sudo("buildslave create-slave %s" % parameters, user="www-data")
#            sudo("mkdir -p %s/%s/builder-build" % (root, base_dir, ), user="www-data")


class Configure(Role):
    """
    Add buildbot Slave for create build package with parameter "repository"
    """
    packages = [ 'build-essential'
        , 'python-dev'
        , 'python-setuptools'
        , 'subversion'
    ]

    def configure(self, server):
        try:
            repository, ec2_master_host, project_name = splitter(self.parameter)
        except ValueError:
            repository, project_name = splitter(self.parameter)
            ec2_master_host = 'localhost'

        root = home(project_name)

        tag_on_slave = 'slave-build'

        slave_virtenv = slave_build_virtual_env_path(root)
        install_buildbot_slave_env(server, slave_virtenv)
        tag(server, tag_on_slave, 'env-installed')

#        setup_buildbot_slave_build(server, root, tag_on_slave, ec2_master_host)

        slave_path = slave_build_location(root)
        slave_checkout_path = "%s/builder-build" % (slave_path)
        svn_checkout(server, slave_checkout_path, repository)
#        setup_library(server, '%s/src/setup/requirelibs.txt' % (slave_checkout_path))
        tag(server, tag_on_slave, 'ready')

