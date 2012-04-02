from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from profab.role import Role
from proteus.buildbot import home
from proteus.buildbot_slave import slave_virtual_env_path, slave_location

def restart_buildbot_slave(server, project_name):
    root = home(project_name)
    env_path = slave_virtual_env_path(root)
    slave_path = slave_location(root)
    if exists(slave_path):
        if exists(env_path):
            with prefix('source %s/bin/activate' % (env_path)):
                sudo('buildslave restart %s' % (slave_path), user='www-data')


class Configure(Role):
    '''
    Restart Buildbot Slave
    '''
    def configure(self, server):
        project_name = self.parameter
        restart_buildbot_slave(server, project_name)

