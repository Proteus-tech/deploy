from profab.role import Role
from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from proteus.buildbot import splitter

def check_config(server, master_config_file, buildbot_master_virtenv):
    if exists(master_config_file):
        if exists(buildbot_master_virtenv):
            with prefix('source %s/bin/activate' % (buildbot_master_virtenv)):
                result = run('buildbot checkconfig %s' % (master_config_file))                      
                if 'Config file is good' not in result:
                    print "Something wrong with master.cfg, Buildbot won't start properly."


class Configure(Role):
    '''
    Check Buildbot Master Configuration file from 
        "full_path_to_master_config_file,full_path_to_buildbot_master_virtenv"
    '''
    def configure(self, server):
        master_config_file, buildbot_master_virtenv = splitter(self.parameter)
        check_config(master_config_file, buildbot_master_virtenv)

