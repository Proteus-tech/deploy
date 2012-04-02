from profab.role import Role
from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from proteus.buildbot import home
from proteus.buildbot_master import master_virtual_env_path, master_location

def update_master_cfg(server, path_to_update):
    sudo(path_to_update, user='www-data')

def restart_buildbot_master(server, project_name):
    root = home(project_name)
    buildbot_master_virtenv = master_virtual_env_path(root)
    buildbot_master_path = master_location(root)
    script_update_master_path = '%s/src/bin/update_master_config' % (root)
    if exists(buildbot_master_path):
        # Do update master config if script update_master_config is valid.
        if exists(script_update_master_path):
            update_master_cfg(script_update_master_path)
        if exists(buildbot_master_virtenv):
            with prefix('source %s/bin/activate' % (buildbot_master_virtenv)):
                sudo('buildbot restart %s' % (buildbot_master_path), user='www-data')

class Configure(Role):
    '''
    Restart Buildbot Master
    '''  
    def configure(self, server):
        project_name = self.parameter
        restart_buildbot_master(server, project_name)

