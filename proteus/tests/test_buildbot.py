import buildbot
from unittest import TestCase

class TestVirtualEnvPath(TestCase):
    def test_virtual_env_path(self):
        project_name = 'fluffy'
        self.assertEqual('/home/www-data/Buildbot/fluffy/virtenv', buildbot.virtual_env_path(project_name))

