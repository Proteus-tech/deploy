from profab.role import Role
from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from proteus.buildbot import splitter

class Configure(Role):
    '''
    Start Buildbot Master with parameters "buildbot_master_path,buildbot_master_virtenv" 
    '''
    def configure(self, server):
        buildbot_master_path, buildbot_master_virtenv = splitter(self.parameter)
        if exists(buildbot_master_path):
            if exists(buildbot_master_virtenv):
                with prefix('source %s/bin/activate' % (buildbot_master_virtenv)):
                    sudo('buildbot start %s' % (buildbot_master_path), user='www-data')
      
