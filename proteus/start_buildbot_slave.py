from profab.role import Role
from fabric.operations import run, sudo
from fabric.context_managers import prefix
from fabric.contrib.files import exists
from proteus.buildbot import splitter

class Configure(Role):
    '''
    Start Buildbot Slave with parameters "buildbot_slave_path,buildbot_slave_virtenv" 
    '''
    def configure(self, server):
        buildbot_slave_path, buildbot_slave_virtenv = splitter(self.parameter)
        if exists(buildbot_slave_path):
            if exists(buildbot_slave_virtenv):
                with prefix('source %s/bin/activate' % (buildbot_slave_virtenv)):
                    sudo('buildslave start %s' % (buildbot_slave_path), user='www-data')
      
