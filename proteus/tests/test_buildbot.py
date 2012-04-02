from proteus import buildbot
from unittest import TestCase

class TestBuildbotCommonFunctions(TestCase):
    def test_buildbot_home(self):
        project_name = 'fluffy'
        root = buildbot.home(project_name)
        self.assertEqual('/home/www-data/Buildbot/fluffy', root)

    def test_virtual_env_path(self):
        root = '/home/www-data/Buildbot/fluffy'
        self.assertEqual('/home/www-data/Buildbot/fluffy/virtenv', buildbot.virtual_env_path(root))

    def test_splitter(self):
        parameters = '/home/www-data/Buildbot/fluffy/buildslave1/builder-sqlite,git@github.com:Proteus-tech/deploy.git'
        expected = ['/home/www-data/Buildbot/fluffy/buildslave1/builder-sqlite', 'git@github.com:Proteus-tech/deploy.git']
        results = buildbot.splitter(parameters)
        self.assertEqual(expected, results)
