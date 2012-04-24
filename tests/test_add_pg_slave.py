from subprocess import call
from unittest import TestCase
import os
import shutil
import tempfile

class TestAddPostgresSlave(TestCase):
    def setUp(self):
        self.origin_path = os.getcwd()
        self.path_check = 'tmp'      
        self.path_bb_slave = '%s/fakeproject/buildbot_config/slaves'  

    def tearDown(self):
        os.chdir(self.origin_path)
        if os.path.exists(self.path_check):
            shutil.rmtree(self.path_check)
            
    def test_create_pg_slave_file(self):
        os.makedirs(self.path_bb_slave % (self.path_check))
        os.chdir('%s/fakeproject' % (self.path_check))
        call( ['../../bin/add-pg-slave-to-master-cfg'] )
        self.assertTrue(os.path.exists('buildbot_config/slaves/pg_slave.py'))
        try:
            with open('buildbot_config/slaves/pg_slave.py') as stream:
                content = stream.read()
                self.assertTrue("nickname = 'pg'" in content)
        except IOError:
            self.fail('buildbot_config/slaves/pg_slave.py not found')

    def test_create_pg_slave_with_parameter(self):
        os.makedirs(self.path_bb_slave % (self.path_check))
        os.chdir('%s/fakeproject' % (self.path_check))
        param = 'mongo'
        call( ['../../bin/add-pg-slave-to-master-cfg',param] )
        self.assertTrue(os.path.exists('buildbot_config/slaves/pg_slave.py'))
        try:
            with open('buildbot_config/slaves/pg_slave.py') as stream:
                content = stream.read()
                self.assertTrue("nickname = '%s'" % (param) in content)
        except IOError:
            self.fail('buildbot_config/slaves/pg_slave.py not found')
 
    def test_runtest_command(self):
        os.makedirs(self.path_bb_slave % (self.path_check))
        os.chdir('%s/fakeproject' % (self.path_check))
        param = 'mongo'
        call( ['../../bin/add-pg-slave-to-master-cfg',param] )
        self.assertTrue(os.path.exists('buildbot_config/slaves/pg_slave.py'))
        try:
            with open('buildbot_config/slaves/pg_slave.py') as stream:
                content = stream.read()
                self.assertTrue('''["/bin/bash","runtests", "--settings=%s_project.settings.pg_buildbot" % PROJECT_NAME, "--noinput"]''' in content)
        except IOError:
            self.fail('buildbot_config/slaves/pg_slave.py not found')
       
