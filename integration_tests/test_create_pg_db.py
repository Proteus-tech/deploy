from fabric.api import settings
from fabric.context_managers import prefix
from fabric.contrib.files import sed
from fabric.operations import sudo, run
from os.path import abspath
from profab.server import Server
from proteus.install_buildbot_slave_env import install_buildbot_slave_env
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

        # clean previous step
        os.system('rm -rf /tmp/proteus-deploy-int/')
        os.system('rm -rf /tmp/easy_install-*')

        tmp_path = os.getcwd()
        os.chdir('..')
        os.system('virtualenv /tmp/proteus-deploy-int')
        activate_this = '/tmp/proteus-deploy-int/bin/activate_this.py'
        execfile(activate_this, dict(__file__=activate_this))
        os.system('python setup.py install')
        os.system('pip install nose')
        os.chdir(tmp_path)
       
        cls.create_simple_server()
        #cls.connect_to_server('ec2-184-72-29-114.us-west-1.compute.amazonaws.com')

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
#        self.delete_buildbot_folder()
        os.system('rm -rf /tmp/proteus-deploy-int/')
        os.system('rm -rf /tmp/easy_install-*')

    def delete_buildbot_folder(self):
        with settings(host_string=self.host_string):
            sudo('rm -rf /home/www-data/Buildbot')

    def test_create_pg_db(self):
        # Arrange
        slave_virtual_env_path = '/home/www-data/Buildbot/hobby/virtenv-slave'

        '''0.run role postgres
        '''
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

        ''' 1.run role install_buildbot_slave_env
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.install_buildbot_slave_env'
            , slave_virtual_env_path]) 
        # Assert
        with settings(host_string=self.host_string):
            # test have slave env slave on server
            output = sudo('ls /home/www-data/Buildbot/hobby')
            self.assertTrue('virtenv-slave' in output)

        ''' 2.run role setup_buildbot_pg_slave
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.setup_buildbot_pg_slave'
            , '/home/www-data/Buildbot/hobby,slave-pg,localhost']) 
        # Assert
        with settings(host_string=self.host_string):
            # test directory is created
            output = sudo('ls /home/www-data/Buildbot/hobby/buildslave1')
            self.assertTrue('builder-pg' in output)
            # test file is changed
            output = sudo('cat /home/www-data/Buildbot/hobby/buildslave1/buildbot.tac')
            self.assertTrue("slavename = 'slave-pg'" in output)
            self.assertTrue("passwd = 'slave-pgpassword'" in output)
        
        ''' 3.run role git_checkout
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.git_checkout'
            , '/home/www-data/Buildbot/hobby/buildslave1/builder-pg,git://github.com/juacompe/hobby.git']) 
        # Assert
        with settings(host_string=self.host_string):
            # test directory is created
            output = sudo('ls /home/www-data/Buildbot/hobby/buildslave1/builder-pg')
            self.assertTrue('src' in output)
            output = sudo('ls /home/www-data/Buildbot/hobby/buildslave1/builder-pg/bin')
            self.assertTrue('update_master_config' in output)
        
        ''' 4.run role setup_library
        '''
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.setup_library'
            , '/home/www-data/Buildbot/hobby/buildslave1/builder-pg/src/setup/requirelibs.txt']) 
        # Assert
        with settings(host_string=self.host_string):
            # test package is installed
            output = sudo('aptitude search libpq-dev')
            self.assertTrue('i   libpq-dev' in output)
            output = sudo('aptitude search build-essential')
            self.assertTrue('i   build-essential' in output)
            output = sudo('aptitude search libpng-dev')
            self.assertTrue('v   libpng-dev' in output)
            output = sudo('aptitude search libjpeg-dev')
            self.assertTrue('v   libjpeg-dev' in output)
            output = sudo('aptitude search python-dev')
            self.assertTrue('i   python-dev' in output)
            output = sudo('aptitude search python-setuptools')
            self.assertTrue('i   python-setuptools' in output)

        ''' 5.run role setup_psycopg2_on_slave
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.setup_psycopg2_on_slave'
            , 'hobby,/home/www-data/Buildbot/hobby/buildslave1/builder-pg']) 
        # Assert
        with settings(host_string=self.host_string):
            # test have psycopg2 in server
            activate = 'source %s/bin/activate' % slave_virtual_env_path
            with prefix(activate):
                output = sudo('pip freeze')
                self.assertTrue('psycopg2' in output)
                
        '''7.run role replace_pg_hba_conf
        '''
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
        
        ''' 8. run role create_pg_db'
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.create_pg_db'
            , 'hobby,git://github.com/juacompe/hobby.git']) 
        # Assert
        with settings(host_string=self.host_string):
            # test user is created
            output = run('psql -c "\l" -A')
            self.assertTrue('hobbyuser' in output)
            # test database is created
            self.assertTrue('hobby' in output)

