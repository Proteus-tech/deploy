from mock import patch, Mock
from proteus.buildbot_master import (master_virtual_env_path
    , master_location, Configure)
from unittest import TestCase

class TestBuildbotMaster(TestCase):
    def test_master_virtual_env_path(self):
        root = '/home/www-data/Buildbot/fluffy'
        path = master_virtual_env_path(root) 
        expected = '/home/www-data/Buildbot/fluffy/virtenv-master'
        self.assertEqual(expected, path)

    def test_master_location(self):
        root = '/home/www-data/Buildbot/fluffy'
        path = master_location(root) 
        expected = '/home/www-data/Buildbot/fluffy/buildbot-master'
        self.assertEqual(expected, path)


class TestMasterConfig(TestCase):
    def setUp(self):
        self.patch_check = patch('proteus.buildbot_master.check_config')
        self.patch_check.start()
        self.patch_complete = patch('proteus.buildbot_master.complete_master_config')
        self.mock_complete = self.patch_complete.start()
        self.patch_symlink = patch('proteus.buildbot_master.create_symlink')
        self.mock_symlink = self.patch_symlink.start()
        self.patch_install_env = patch('proteus.buildbot_master.install_buildbot_master_env')
        self.patch_install_env.start()
        self.patch_checkout = patch('proteus.buildbot_master.git_checkout')
        self.patch_checkout.start()
        self.patch_setup = patch('proteus.buildbot_master.setup_buildbot_master')
        self.patch_setup.start()
        self.patch_tag = patch('proteus.buildbot_master.tag')
        self.patch_tag.start()
        
    def test_master_config_is_symlink(self):
        """
        master.cfg needs to be a symbolic link to src/buildbot/master.cfg
        so that when a developer commits updated one, the file on server
        also updates
        """
        # Arrange
        role = Configure()
        role.parameter = repository = 'https://juacompe@github.com/juacompe/fluffy.git'
        server = Mock()
        # Act
        role.configure(server)
        # Assert
        self.mock_symlink.assert_called_once_with(server
            , '/home/www-data/Buildbot/fluffy/src/buildbot/master.cfg'
            , '/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg'
        )
        
    def test_complete_config_with_master_in_repository(self):
        """
        Scenario: execute role proteus.buildbot_master with parameter
        https://juacompe@github.com/juacompe/fluffy.git

        Expected:
        - complete_master_config is called with 
          /home/www-data/Buildbot/fluffy/src/buildbot/master.cfg 
          as parameter

        sed command overrides the file with a new one; therefore, we
        cannot use sed command on the symlink file 
        (i.e. /home/www-data/Buildbot/fluffy/buildbot-master/master.cfg) 
        or the link will be broken.

        we need to update the source in repository instead 
        (i.e. /home/www-data/Buildbot/fluffy/src/buildbot/master.cfg)
        """
        # Arrange
        role = Configure()
        role.parameter = repository = 'https://juacompe@github.com/juacompe/fluffy.git'
        server = Mock()
        # Act
        role.configure(server)
        # Assert
        self.mock_complete.assert_called_once_with(server
            , '/home/www-data/Buildbot/fluffy/src/buildbot/master.cfg'
            , repository
        )
        
