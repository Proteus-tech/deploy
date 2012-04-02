from profab.role import Role
from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from proteus.buildbot import home
from proteus.buildbot_master import master_virtual_env_path, master_location 

def start_buildbot_master(server, project_name):
    root = home(project_name) 
    buildbot_master_path = master_location(root) 
    buildbot_master_virtenv = master_virtual_env_path(root)
    if exists(buildbot_master_path):
        if exists(buildbot_master_virtenv):
            with prefix('source %s/bin/activate' % (buildbot_master_virtenv)):
                sudo('buildbot start %s' % (buildbot_master_path), user='www-data')
      
    
class Configure(Role):
    '''
    Start Buildbot Master with parameters "buildbot_master_path,buildbot_master_virtenv" 
    '''
    def configure(self, server):
        project_name = self.parameter
        start_buildbot_master(server, project_name)
