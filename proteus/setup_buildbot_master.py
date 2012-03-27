from buildbot import virtual_env_path
from fabric.context_managers import cd, prefix
from fabric.operations import run, sudo
from profab.role import Role

class Configure(Role):
    """
    Setup Buildbot Master with parameter "root"
    """
    def configure(self, server):
        root = self.parameter
        virtenv_path = '%s-master' % virtual_env_path(root)
        with prefix("source %s/bin/activate" % (virtenv_path)):
            with cd(root):
                sudo("buildbot create-master buildbot-master", user="www-data")

