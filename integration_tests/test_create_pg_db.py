#!usr/bin/python
from fabric.api import settings
from fabric.context_managers import prefix
from fabric.contrib.files import sed
from fabric.operations import sudo, local, run
from os.path import abspath
from profab.server import Server, _on_this_server
from proteus.install_buildbot_master_env import install_buildbot_master_env
from subprocess import call
from unittest import TestCase
import sys, os

class TestCreatePgDb(TestCase):
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
        '''
        create virtual environment for run integration test
        start simple server
        '''
        tmp_path = os.getcwd()
        os.chdir('..')
        os.system('. ~/.bashrc')
        os.system('virtualenv /tmp/proteus-deploy-int')
        activate_this = '/tmp/proteus-deploy-int/bin/activate_this.py'
        execfile(activate_this, dict(__file__=activate_this))
        os.system('python setup.py install')
        os.system('pip install nose')
        os.chdir(tmp_path)
       
        cls.create_simple_server()
        #cls.connect_to_server('ec2-50-18-15-96.us-west-1.compute.amazonaws.com')

    @classmethod
    def tearDownClass(cls):
        '''
        delete environment and unuse folder
        terminate server
        '''
        os.system('rm -rf /tmp/proteus-deploy-int/')
        os.system('rm -rf ../build/ ../dist/ ../proteus_deploy.egg-info/')
        cls.server.stop()
        cls.server.terminate()
        
    def setUp(self):
        self.ec2_host = self.server.instance.dns_name
        self.host_string = 'ubuntu@%s' % self.ec2_host
        
    def tearDown(self):
        self.delete_buildbot_folder()
        pass

    def delete_buildbot_folder(self):
        with settings(host_string=self.host_string):
            sudo('rm -rf /home/www-data/Buildbot')

    def test_setup_buildbot_master_env(self):
        # Arrange
        master_virtual_env_path = '/home/www-data/Buildbot/hobby/virtenv-master'
        # Act
        call(['setup-buildbot-on-server'
            , 'proteus'
            , self.ec2_host
            , 'hobby'
            , 'git://github.com/juacompe/hobby.git']) 
        # Assert
        with settings(host_string=self.host_string):
            # test have postgresql in server
            output = sudo('ls /home/www-data/Buildbot/')
            self.assertTrue('hobby' in output)

        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , 'postgres']) 
        # Assert
        with settings(host_string=self.host_string):
            # test have postgresql in server
            output = sudo('ls /etc/')
            self.assertTrue('postgresql' in output)
        
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.setup_psycopg2_on_slave'
            , 'hobby']) 
        # Assert
        with settings(host_string=self.host_string):
            # test have psycopg2 in server
            output = sudo('pip freeze')
            self.assertTrue('psycopg2' in output)
        
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , 'proteus.replace_pg_hba_conf']) 
        # Assert
        with settings(host_string=self.host_string):
            # test pg_hba.conf is modified
            output = sudo('cat /etc/postgresql/8.4/main/pg_hba.conf')
            self.assertTrue('local   all all             trust' in output)
            self.assertTrue('host    all all     127.0.0.1/32    md5' in output)    
        
        # Assert
        with settings(host_string=self.host_string):
            # test rename folder
            sudo('mv /home/www-data/Buildbot/hobby/buildslave1/builder-sqlite/'
                 ' /home/www-data/Buildbot/hobby/buildslave1/builder-pg/')
            output = sudo('ls /home/www-data/Buildbot/hobby/buildslave1/')
            self.assertTrue('builder-pg' in output)
        
        # Assert
        with settings(host_string=self.host_string):
            # test fix file buildbot.tac
            sed('/home/www-data/Buildbot/hobby/buildslave1/buildbot.tac'
                , "slave-sqlite"
                , "slave-pg"
                , use_sudo=True)
            sed('/home/www-data/Buildbot/hobby/buildslave1/buildbot.tac'
                , "slave-sqlitepassword"
                , "slave-pgpassword"
                , use_sudo=True)
            output = sudo('cat /home/www-data/Buildbot/hobby/buildslave1/buildbot.tac')
            self.assertTrue("slavename = 'slave-pg'" in output)
            self.assertTrue("passwd = 'slave-pgpassword'" in output)
        
        # Act
        call(['restart-buildbot-master'
            , 'proteus'
            , self.ec2_host
            , 'hobby'])      
        call(['restart-buildbot-slave'
            , 'proteus'
            , self.ec2_host
            , 'hobby']) 
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.create_pg_db'
            , 'hobby']) 
        # Assert
        with settings(host_string=self.host_string):
            # test user is created
            output = run('psql -c "\l" -A')
            self.assertTrue('hobbyuser' in output)
            # test database is created
            self.assertTrue('hobby' in output)
