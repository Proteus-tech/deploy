from fabric.api import settings
from fabric.context_managers import prefix
from fabric.operations import sudo
from os.path import abspath
from profab.server import Server, _on_this_server
from proteus.install_buildbot_master_env import install_buildbot_master_env
from subprocess import call
from unittest import TestCase
import sys

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
        #cls.server = Server.start('proteus', *role_tuple_list)
        cls.server = Server.connect('proteus', 'ec2-184-72-4-120.us-west-1.compute.amazonaws.com')
        assert cls.server, 'Server should be connected'

    @classmethod
    def setUpClass(cls):
        cls.create_simple_server()

    @classmethod
    def tearDownClass(cls):
        pass
        #cls.server.terminate()
        
    def delete_buildbot_folder(self):
        with settings(host_string=host_string):
            sudo('rm -rf /home/www-data/Buildbot')

    def test_setup_buildbot_master_env(self):
        # Arrange
        master_virtual_env_path = '/home/www-data/Buildbot/hobby/virtenv-master'
        # Act
        # TODO call from script to test script too
        ec2_host = self.server.instance.dns_name
        #call(['pf-server-role-add'
        #    , 'proteus'
        #    , ec2_host
        #    , '--proteus.install_buildbot_master_env'
        #    , master_virtual_env_path]) 
        remote_function = _on_this_server(install_buildbot_master_env)
        remote_function(self.server, master_virtual_env_path)
        # Assert
        host_string = 'ubuntu@%s' % ec2_host
        with settings(host_string=host_string):
            activate = 'source %s/bin/activate' % master_virtual_env_path
            with prefix(activate):
                output = sudo('env | grep virtenv-master')
                self.assertTrue('VIRTUAL_ENV=/home/www-data/Buildbot/hobby/virtenv-master' in output)

