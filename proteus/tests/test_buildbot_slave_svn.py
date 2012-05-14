from proteus.buildbot_slave_svn import slave_virtual_env_path, slave_location
from unittest import TestCase

class TestBuildbotSlave(TestCase):
    def test_slave_virtual_env_path(self):
        root = '/home/www-data/Buildbot/fluffy'
        path = slave_virtual_env_path(root) 
        expected = '/home/www-data/Buildbot/fluffy/virtenv-slave'
        self.assertEqual(expected, path)

    def test_slave_location(self):
        root = '/home/www-data/Buildbot/fluffy'
        path = slave_location(root) 
        expected = '/home/www-data/Buildbot/fluffy/buildslave1'
        self.assertEqual(expected, path)

