from profab.role import Role
from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from proteus.buildbot import home
from proteus.buildbot_master import master_virtual_env_path, master_location 

def control_buildbot_master(sever, project_name, command):
    root = home(project_name) 
    master_src = '%s/src' % root
    buildbot_master_path = master_location(root) 
    buildbot_master_virtenv = master_virtual_env_path(root)
    if not exists(buildbot_master_path):
        raise Exception('Buildbot master not found: %s' % buildbot_master_path)
    if not exists(buildbot_master_virtenv):
        raise Exception('Master environement not found: %s' % buildbot_master_virtenv)
    with prefix('source %s/bin/activate' % (buildbot_master_virtenv)):
        export = 'export PYTHONPATH=%s' % (master_src)
        control_buildbot = 'buildbot %s %s' % (command, buildbot_master_path)
        sudo('%s && %s' % (export, control_buildbot), user='www-data')
 
def start_buildbot_master(server, project_name):
    control_buildbot_master(server, project_name, 'start')
     
    
class Configure(Role):
    '''
    Start Buildbot Master with parameters "buildbot_master_path,buildbot_master_virtenv" 
    '''
    def configure(self, server):
        project_name = self.parameter
        start_buildbot_master(server, project_name)
