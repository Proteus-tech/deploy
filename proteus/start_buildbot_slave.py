from profab.role import Role
from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from proteus.buildbot import home
from proteus.buildbot_slave import slave_virtual_env_path, slave_location 

def start_buildbot_slave(server, project_name):
    root = home(project_name) 
    buildbot_slave_path = slave_location(root) 
    buildbot_slave_virtenv = slave_virtual_env_path(root)
    if exists(buildbot_slave_path):
        if exists(buildbot_slave_virtenv):
            with prefix('source %s/bin/activate' % (buildbot_slave_virtenv)):
                sudo('buildslave start %s' % (buildbot_slave_path), user='www-data')
      

class Configure(Role):
    '''
    Start Buildbot Slave with parameters "buildbot_slave_path,buildbot_slave_virtenv" 
    '''
    def configure(self, server):
        project_name = self.parameter
        start_buildbot_slave(server, project_name)

