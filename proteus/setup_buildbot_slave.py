from buildbot import virtual_env_path
from fabric.context_managers import cd, prefix
from fabric.operations import run, sudo
from profab.role import Role
from proteus import buildbot

class Configure(Role):
    """
    Setup Buildbot Slave with parameter "project_name,name,master_host"
    """
    def configure(self, server):
        project_name, name, master_host = buildbot.splitter(self.parameter)
        virtenv_path = '%s-slave' % virtual_env_path(project_name)
        base_dir = 'build%s' % name
        password = '%spassword' % name 
        parameters = "%s %s %s %s" % (base_dir, master_host, name, password)
        with prefix("source %s/bin/activate" % (virtenv_path)):
            with cd("/home/www-data/Buildbot/%s" % (project_name)):
                sudo("buildslave create-slave %s" % parameters, user="www-data")

