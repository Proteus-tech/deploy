from profab.role import Role
from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from proteus.buildbot import master_virtual_env_path, home, master_location

def check_config(server, master_config_file, buildbot_master_virtenv, master_src):
    if not exists(master_config_file):
        raise Exception('Master config file not found: %s' % master_config_file)
    if not exists(buildbot_master_virtenv):
        raise Exception('Master environement not found: %s' % buildbot_master_virtenv)
    with prefix('source %s/bin/activate' % (buildbot_master_virtenv)):
        export = 'export PYTHONPATH=%s' % (master_src)
        checkconfig = 'buildbot checkconfig %s' % (master_config_file)
        result = run('%s && %s' % (export, checkconfig))                      
        if 'Config file is good' not in result:
            raise Exception("Something wrong with master.cfg, Buildbot won't start properly.")


class Configure(Role):
    '''
    Check Buildbot Master Configuration file from 
        "project_name"
    '''
    def configure(self, server):
        project_name = self.parameter
        root = home(project_name)
        buildbot_master_virtenv = master_virtual_env_path(root)
        master_path = master_location(root) 
        master_config_file = '%s/master.cfg' % (master_path)
        master_src = '%s/src' % root
        check_config(server, master_config_file, buildbot_master_virtenv, master_src)

