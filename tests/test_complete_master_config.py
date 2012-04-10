from unittest import TestCase
import os, shutil

class TestCompleteMasterConfig(TestCase):
    def tearDown(self):
        if os.path.exists('master.tmp'):
            shutil.copyfile('master.tmp', 'buildbot/master.cfg')
            os.remove('master.tmp')
        os.chdir('../')
    
    def setUp(self):
        os.chdir('project_template')
        shutil.copyfile('buildbot/master.cfg', 'master.tmp')
    
    def test_complete_master_config(self):
        # Arrange
        ec2_host = 'ec2-50-18-236-118.us-west-1.compute.amazonaws.com' 
        repository = 'git://github.com/juacompe/fluffy.git'
        # Act
        os.system('../bin/complete_master_config %s %s' % (ec2_host, repository))
        # Assert
        try:
            with open('buildbot/master.cfg') as stream:
                content = stream.read()
                self.assertTrue('ec2-50-18-236-118.us-west-1.compute.amazonaws.com' in content)
                self.assertTrue('git://github.com/juacompe/fluffy.git' in content)
                self.assertTrue('src' in content)

                self.assertTrue('/path/to/repo' not in content)
                self.assertTrue('project_dirname' not in content)
                self.assertTrue('buildbot_master_host' not in content)

        except IOError:
            self.fail('master.cfg is missing, can not config file')
     
