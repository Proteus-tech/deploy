from fabric.operations import sudo
from fabric.api import cd, run
from fabric.contrib.files import exists
from profab.role import Role
from fabric.context_managers import prefix
from buildbot import slave_virtual_env_path, home
from profab import _logger

def setup_psycopg2_on_slave(server, project_name):
    '''
    Process
        1. check if virtual env exists.
        2. activate that virtual env.
    '''
    bb_virtual_env = "/home/www-data/Buildbot/%s/virtenv-slave" % (project_name)
    root = home(project_name)
    bb_virtual_env = slave_virtual_env_path(root)
    if exists(bb_virtual_env):
        with prefix("source %s/bin/activate" % (bb_virtual_env)):
            sudo("pip install psycopg2==2.4.1", user="www-data")
            result = sudo("pip freeze", user="www-data")
            if "psycopg2" not in result:
                raise Exception("psycopg2 does not install in %s" % (bb_virtual_env))
            else:
                print "psycopg2 installed in %s" % (bb_virtual_env)

class Configure(Role):
    """
    Install psycopg2 package fixed for version 2.4.1

    - take input parameter
        project-name , then role would find virtenv-slave to activate 

    - require
        postgres package installed
    """
    
    packages = [
        'python-psycopg2'
    ]

    def configure(self, server):
        setup_psycopg2_on_slave(server, self.parameter)
                     
