#!/usr/bin/env python
from fabric.context_managers import cd, prefix
from fabric.operations import sudo
from fabric.contrib.files import exists

from profab.role import Role
from proteus.buildbot import virtual_env_path, home, splitter
from proteus.svn_checkout import root_folder, svn_checkout
from proteus.install_buildbot_slave_env import install_buildbot_slave_env
from proteus.setup_buildbot_slave import setup_buildbot_slave
from proteus.tag import tag
from profab import _logger


TAG_ON_SL = 'slave-build'
BASE_DIR = 'buildslave1-build'
PROTEUS_DEPLOY_GIT_URL = 'git@github.com:Proteus-tech/deploy.git@deploy'


def slave_build_virtual_env_path(root):
    virtenv_path = virtual_env_path(root)
    return '%s-slave-build' % virtenv_path


def slave_build_location(root):
    return '%s/%s' % (root, BASE_DIR)


def setup_buildbot_slave_build(server, root, name, master_host):
    virtenv_path = '%s-slave-build' % virtual_env_path(root)
    base_dir = BASE_DIR
    password = '%spassword' % name
    parameters = "%s %s %s %s" % (base_dir, master_host, name, password)
    with prefix("source %s/bin/activate" % (virtenv_path)):
        with cd(root):
            sudo("buildslave create-slave %s" % parameters, user="www-data")
            sudo(
                "mkdir -p %s/%s/builder-build" % (root, base_dir),
                user="www-data"
            )


def setup_proteus_deploy_on_virtenv(server, path_to_virtenv):
    if exists(path_to_virtenv):
        with prefix("source %s/bin/activate" % path_to_virtenv):
            sudo("pip install git+%s" % PROTEUS_DEPLOY_GIT_URL, user="www-data")
            _logger.info("Done, setting up proteus-deploy")
    else:
        _logger.error("%s does not exist.", path_to_virtenv)


class Configure(Role):
    """Add buildbot Slave for create build package with parameter "repository"
    """
    packages = [
        'build-essential',
        'python-dev',
        'python-setuptools',
        'subversion'
    ]

    def configure(self, server):
        param = self.parameter
        try:
            repository, ec2_master_host, project_name = splitter(param)
        except ValueError:
            repository, project_name = splitter(param)
            ec2_master_host = 'localhost'

        root = home(project_name)

        # Create virtenv for buildbot slave.
        slave_virtenv = slave_build_virtual_env_path(root)
        install_buildbot_slave_env(server, slave_virtenv)
        tag(server, TAG_ON_SL, 'env-installed')

        # Create buildbot slave base folder and builder folder.
        setup_buildbot_slave_build(server, root, TAG_ON_SL, ec2_master_host)

#        slave_path = slave_build_location(root)
#        slave_checkout_path = "%s/builder-build" % (slave_path)
#        svn_checkout(server, slave_checkout_path, repository)
        setup_proteus_deploy_on_virtenv(server, slave_virtenv)
        tag(server, TAG_ON_SL, 'ready')
