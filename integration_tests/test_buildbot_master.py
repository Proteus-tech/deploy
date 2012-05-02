#!usr/bin/python
from fabric.api import settings
from fabric.context_managers import prefix
from fabric.operations import sudo, local
from os.path import abspath
from profab.server import Server
from proteus.install_buildbot_master_env import install_buildbot_master_env
from subprocess import call
from unittest import TestCase
import sys, os

class TestBuildbotMaster(TestCase):
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
        #pass

    @classmethod
    def setUpClass(cls):
        '''
        create virtual environment for run integration test
        start simple server
        '''

        # clean previous step
        target_dir = '/tmp/proteus-deploy-int'
        if os.path.exists(target_dir)
            os.system('rm -rf %s' % (target_dir))

        tmp_path = os.getcwd()
        os.chdir('..')
        os.system('virtualenv /tmp/proteus-deploy-int')
        activate_this = '/tmp/proteus-deploy-int/bin/activate_this.py'
        execfile(activate_this, dict(__file__=activate_this))
        os.system('python setup.py install')
        os.system('pip install nose')
        os.chdir(tmp_path)
       
        cls.create_simple_server()
        #cls.connect_to_server('ec2-50-18-1-24.us-west-1.compute.amazonaws.com')

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

    def delete_buildbot_folder(self):
        with settings(host_string=self.host_string):
            sudo('rm -rf /home/www-data/Buildbot')

    def test_setup_buildbot_master_env(self):
        # Arrange
        master_virtual_env_path = '/home/www-data/Buildbot/hobby/virtenv-master'
        # Act
        # TODO call from script to test script too
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.install_buildbot_master_env'
            , master_virtual_env_path]) 
        #remote_function = _on_this_server(install_buildbot_master_env)
        #remote_function(self.server, master_virtual_env_path)
        # Assert
        with settings(host_string=self.host_string):
            activate = 'source %s/bin/activate' % master_virtual_env_path
            with prefix(activate):
                # test that environment can be activated
                output = sudo('env | grep virtenv-master')
                self.assertTrue('VIRTUAL_ENV=/home/www-data/Buildbot/hobby/virtenv-master' in output)
                # test that environment contains buildbot package
                output = sudo('pip freeze')
                self.assertTrue('buildbot' in output)
