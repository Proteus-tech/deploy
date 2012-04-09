from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from profab.role import Role
from proteus.buildbot import home
from proteus.buildbot_slave import slave_virtual_env_path, slave_location
from proteus.start_buildbot_slave import control_buildbot_slave

def restart_buildbot_slave(server, project_name):
    control_buildbot_slave(server, project_name, 'restart')


class Configure(Role):
    '''
    Restart Buildbot Slave
    '''
    def configure(self, server):
        project_name = self.parameter
        restart_buildbot_slave(server, project_name)

