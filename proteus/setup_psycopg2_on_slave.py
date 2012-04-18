from fabric.operations import sudo
from fabric.api import cd, run
from fabric.contrib.files import exists
from profab.role import Role
from fabric.context_managers import prefix
from buildbot import home
from buildbot_slave import slave_virtual_env_path
from profab import _logger

def setup_psycopg2_on_slave(server, virtual_env_path):
    '''
    Take
        1. path of virtual environment.
    Process
        1. check if virtual env exists.
        2. activate that virtual env.
    '''
    if exists(virtual_env_path):
        with prefix("source %s/bin/activate" % (virtual_env_path)):
            sudo("pip install psycopg2==2.4.1", user="www-data")
            result = sudo("pip freeze", user="www-data")
            if "psycopg2" not in result:
                raise Exception("psycopg2 does not install in %s" % (virtual_env_path))
            else:
                print "psycopg2 installed in %s" % (virtual_env_path)

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
        project_name = self.parameter
        root = home(project_name)
        bb_virtual_env_path = slave_virtual_env_path(root) 
        setup_psycopg2_on_slave(server, bb_virtual_env_path)
                     
