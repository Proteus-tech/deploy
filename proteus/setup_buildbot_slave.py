from buildbot import virtual_env_path
from fabric.context_managers import cd, prefix
from fabric.operations import run, sudo
from profab.role import Role
from proteus import buildbot

def setup_buildbot_slave(slave, root, name, master_host):
    virtenv_path = '%s-slave' % virtual_env_path(root)
    base_dir = 'build%s' % name
    password = '%spassword' % name 
    parameters = "%s %s %s %s" % (base_dir, master_host, name, password)
    with prefix("source %s/bin/activate" % (virtenv_path)):
        with cd(root):
            sudo("buildslave create-slave %s" % parameters, user="www-data")
            sudo("mkdir -p %s/buildslave1/builder-sqlite" % (root), user="www-data")

class Configure(Role):
    """
    Setup Buildbot Slave with parameter "root,name,master_host"
    """
    def configure(self, server):
        root, name, master_host = buildbot.splitter(self.parameter)
        setup_buildbot_slave(server, root, name, master_host)

