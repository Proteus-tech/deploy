from profab.role import Role
from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from proteus.buildbot import home
from proteus.buildbot_master import master_virtual_env_path, master_location

def run_script_update_master_cfg(server, project_name):
    root = home(project_name)
    script_path = '%s/bin/update_master_config' % (root)
    script_with_project_name = '%s %s' % (script_path, project_name)
    if exists(script_path):
        sudo(script_with_project_name, user='www-data')

def restart_buildbot_master(server, project_name):
    root = home(project_name)
    master_src = '%s/src' % root
    buildbot_master_virtenv = master_virtual_env_path(root)
    buildbot_master_path = master_location(root)
    if not exists(buildbot_master_path):
        raise Exception('Buildbot master not found: %s' % buildbot_master_path)
    if not exists(buildbot_master_virtenv):
        raise Exception('Master environement not found: %s' % buildbot_master_virtenv)
    with prefix('source %s/bin/activate' % (buildbot_master_virtenv)):
        export = 'export PYTHONPATH=%s' % (master_src)
        restart = 'buildbot restart %s' % (buildbot_master_path)
        sudo('%s && %s' % (export, restart), user='www-data')

class Configure(Role):
    '''
    Restart Buildbot Master
    '''  
    def configure(self, server):
        project_name = self.parameter
        run_script_update_master_cfg(server, project_name)
        restart_buildbot_master(server, project_name)

