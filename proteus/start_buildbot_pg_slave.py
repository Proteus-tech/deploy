from profab.role import Role
from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from proteus.buildbot import home
from proteus.buildbot_slave import slave_virtual_env_path, slave_location_pg 

def control_buildbot_slave(server, project_name, command):
    root = home(project_name) 
    buildbot_slave_path = slave_location(root) 
    buildbot_slave_virtenv = slave_virtual_env_path(root)
    if not exists(buildbot_slave_path):
        raise Exception('Buildbot slave not found: %s' % buildbot_slave_path)
    if not exists(buildbot_slave_virtenv):
        raise Exception('Slave environment not found: %s' % buildbot_slave_virtenv)
    with prefix('source %s/bin/activate' % (buildbot_slave_virtenv)):
        sudo('buildslave %s %s' % (command, buildbot_slave_path), user='www-data')
 
def start_buildbot_slave(server, project_name):
    control_buildbot_slave(server, project_name, 'start')
         

class Configure(Role):
    '''
    Start Buildbot Slave with parameters "buildbot_slave_path,buildbot_slave_virtenv" 
    '''
    def configure(self, server):
        project_name = self.parameter
        start_buildbot_slave(server, project_name)

