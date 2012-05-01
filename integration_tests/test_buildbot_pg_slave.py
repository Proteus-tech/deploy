from fabric.api import settings
from fabric.context_managers import prefix
from fabric.operations import sudo, local
from fabric.contrib.files import exists
from os.path import abspath
from profab.server import Server 
from proteus.install_buildbot_slave_env import install_buildbot_slave_env
from subprocess import call
from unittest import TestCase
import sys
import os

class TestBuildbotPGSlave(TestCase):
    @classmethod
    def create_simple_server(cls):
        """
        Simulate bin/start-simple-server script by create a new instance using
        roles as simple server script. 
        """
        role_tuple_list = [
              ('security_group','ssh')
            , ('security_group','http')
            , ('wsgi','')
            , ('bits','64')
            , ('region','us-west-1')
            , ('size','t1.micro')
            , ('ami','ami-4d580408')
        ]
        cls.server = Server.start('proteus', *role_tuple_list)
        assert cls.server, 'Server should be connected'

    @classmethod
    def connect_to_server(cls, ec2_host):
        cls.server = Server.connect('proteus', ec2_host)

    @classmethod
    def setUpClass(cls):
        tmp_path = os.getcwd()
        os.chdir('..')
        os.system('virtualenv /tmp/proteus-deploy-int')
        activate_this = '/tmp/proteus-deploy-int/bin/activate_this.py'
        execfile(activate_this, dict(__file__=activate_this))
        os.system('python setup.py install')
        os.system('pip install nose')
        os.chdir(tmp_path)

        cls.create_simple_server()

    @classmethod
    def tearDownClass(cls):
        '''
        delete environment and unuse folder
        terminate server
        '''
        os.system('rm -rf /tmp/proteus-deploy-int/')
        os.system('rm -rf ../build/ ../dist/ ../proteus_deploy.egg-info/')
        
        cls.server.cnx.close()
        cls.server.terminate()

    def setUp(self):
        self.ec2_host = self.server.instance.dns_name
        self.host_string = 'ubuntu@%s' % self.ec2_host

    def tearDown(self):
        self.delete_buildbot_folder()

    def delete_buildbot_folder(self):
        with settings(host_string=self.host_string):
            sudo('rm -rf /home/www-data/Buildbot')

    def test_setup_buildbot_pg_slave(self):
        slave_virtual_env_path = '/home/www-data/Buildbot/hobby/virtenv-slave'

        local('''setup-pg-slave-on-server \
                proteus \
                %s \
                localhost \
                hobby \
                git://github.com/juacompe/hobby.git''' 
                % (self.ec2_host)
        )

        with settings(host_string=self.host_string):
            # check if postres was installed.
            output = sudo('aptitude search postgres')
            self.assertTrue('i   postgresql' in output)
            self.assertTrue('i A postgresql-' in output) 

            activate = 'source %s/bin/activate' % slave_virtual_env_path
            with prefix(activate):
                # check if virtenv-slave is valid.
                output = sudo('env | grep virtenv-slave')
                self.assertTrue('VIRTUAL_ENV=/home/www-data/Buildbot/hobby/virtenv-slave' in output)
                
                # check if buildbot-slave environment was installed.
                output = sudo('pip freeze')
                self.assertTrue('buildbot-slave' in output)

                # check if buildbot slave was installed and git check out work correctly.
                self.assertTrue(exists('/home/www-data/Buildbot/hobby/buildslave1/builder-pg/src'))

                # check if needed libraries were installed.
                output = sudo('aptitude search libpq-dev')
                self.assertTrue('i   libpq-dev' in output)
                output = sudo('aptitude search python-psycopg')
                self.assertTrue('i   python-psycopg' in output)
                
                # check if psycopg2 was already install in virtual-env.
                output = sudo('pip freeze')
                self.assertTrue('psycopg' in output)

            # check if pg_hba.conf was modified correctly.
            linux_codename = sudo('lsb_release -cs')
            if 'natty' in linux_codename:
                pg_version = '8.4'
            elif 'oneiric' in linux_codename:
                pg_version = '9.1'
            else:
                pg_version = '8.4'

            pg_hba_conf_path = '/etc/postgresql/%s/main/pg_hba.conf' % (pg_version)
            output = sudo('cat %s' % (pg_hba_conf_path))
            self.assertTrue('local   all all             trust' in output)
            self.assertTrue('host    all all     127.0.0.1/32    md5' in output)
                    
            # check if postgresdb was created correctly.
            output = sudo("psql -c '\l' -U postgres -A")
            self.assertTrue('hobby|hobbyuser' in output)


