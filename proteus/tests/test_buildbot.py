from proteus import buildbot
from unittest import TestCase

class TestVirtualEnvPath(TestCase):
    def test_virtual_env_path(self):
        root = '/home/www-data/Buildbot/fluffy'
        self.assertEqual('/home/www-data/Buildbot/fluffy/virtenv', buildbot.virtual_env_path(root))


class TestSplitterTest(TestCase):
    def test_splitter(self):
        parameters = '/home/www-data/Buildbot/fluffy/buildslave1/builder-sqlite,git@github.com:Proteus-tech/deploy.git'
        expected = ['/home/www-data/Buildbot/fluffy/buildslave1/builder-sqlite', 'git@github.com:Proteus-tech/deploy.git']
        results = buildbot.splitter(parameters)
        self.assertEqual(expected, results)