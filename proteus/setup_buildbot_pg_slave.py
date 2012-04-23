from buildbot import virtual_env_path
from fabric.context_managers import cd, prefix
from fabric.operations import run, sudo
from profab.role import Role
from proteus import buildbot

def setup_buildbot_pg_slave(slave, root, name, master_host):
    virtenv_path = '%s-slave' % virtual_env_path(root)
    base_dir = 'buildslave1'
    password = '%spassword' % name 
    parameters = "%s %s %s %s" % (base_dir, master_host, name, password)
    with prefix("source %s/bin/activate" % (virtenv_path)):
        with cd(root):
            sudo("buildslave create-slave %s" % parameters, user="www-data")
            sudo("mkdir -p %s/buildslave1/builder-pg" % (root), user="www-data")

class Configure(Role):
    """
    Setup Buildbot Slave with parameter "root,name,master_host"
    """
    def configure(self, server):
        root, name, master_host = buildbot.splitter(self.parameter)
        setup_buildbot_pg_slave(server, root, name, master_host)

