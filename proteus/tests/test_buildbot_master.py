from proteus.buildbot_master import master_virtual_env_path, master_location
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

