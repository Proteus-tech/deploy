from buildbot import virtual_env_path
from fabric.context_managers import cd, prefix
from fabric.operations import run, sudo
from profab.role import Role

class Configure(Role):
    """
    Setup Buildbot Master with parameter "project_name"
    """
    def configure(self, server):
        project_name = self.parameter
        virtenv_path = virtual_env_path(project_name)
        with prefix("source %s/bin/activate" % (virtenv_path)):
            with cd("/home/www-data/Buildbot/%s" % (project_name)):
                sudo("buildbot create-master buildbot-master", user="www-data")

