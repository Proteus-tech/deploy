from fabric.operations import sudo
from fabric.api import cd, run
from fabric.contrib.files import exists
from profab.role import Role
from fabric.context_managers import prefix
from buildbot import home
from buildbot_slave import slave_virtual_env_path, slave_location_pg
from profab import _logger
from proteus import buildbot

def setup_psycopg2_on_slave(server, virtual_env_path, slave_checkout_path):
    '''
    Take
        1. path of virtual environment.
    Process
        1. check if virtual env exists.
        2. activate that virtual env.
    '''
    sudo("apt-get install -y libpq-dev")
    sudo("apt-get install -y python-psycopg2")
    requirements_pg_path = "%s/src/setup/requirements_pg.txt" % (slave_checkout_path)
    if exists(virtual_env_path):
        with prefix("source %s/bin/activate" % (virtual_env_path)):
            if exists(requirements_pg_path):
                sudo("pip install -r %s" % (requirements_pg_path), user="www-data")
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
    
    def configure(self, server):
        project_name, slave_checkout_path = buildbot.splitter(self.parameter)
        root = home(project_name)
        bb_virtual_env_path = slave_virtual_env_path(root) 
        setup_psycopg2_on_slave(server, bb_virtual_env_path, slave_checkout_path)
