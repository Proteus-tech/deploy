from profab.server import Server
from subprocess import call
from unittest import TestCase


   
class TestBuildbotMaster(TestCase):
    @classmethod
    def setupClass(cls):
        role_tuple_list = [
              ('security_group','ssh')
            , ('security_group','http')
            , ('wsgi','')
            , ('bits','64')
            , ('region','us-west-1')
            , ('size','t1.micro')
            , ('ami','ami-4d580408')
            #, ('proteus.www_home','')
            #, ('proteus.install_buildbot_master_env','/home/www-data/Buildbot/fluffy/virtenv-master')                                    
            #, ('proteus.tag','master,env-installed')
        ]
        #cls.server = Server.connect('proteus', 'ec2-184-169-248-190.us-west-1.compute.amazonaws.com')
        cls.server = Server.start('proteus', *role_tuple_list)
        assert cls.server, 'Server should be connected'
        #server.add_roles( server.get_role_adders(*role_tuple_list) )

    @classmethod
    def tearDownClass(cls):
        assert cls.server, 'Server should be connected'
        cls.server.terminate()

    def test_setup_buildbot_master_env(self):
        call(['ls', '-la', '../bin/']) 
        assert self.server, 'Server should be connected'

