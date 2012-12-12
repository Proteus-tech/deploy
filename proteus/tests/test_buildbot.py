from proteus import buildbot
from proteus.buildbot import split_private_git_url
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

    def test_split_svn_url(self):
        # Act
        host = buildbot.split_svn_url('http://vcs.vps.shogunvps.com:8081/scm-webapp-1.14/svn/testsvn/project/trunk')
        # Assert
        self.assertEqual('http://vcs.vps.shogunvps.com', host)

    def test_project_base_folder(self):
        project_name = 'dotto'
        project_base_folder = buildbot.project_base_folder(project_name)
        self.assertEqual('/home/www-data/dotto', project_base_folder)

    def test_split_private_git_url(self):
        user, host, path = split_private_git_url('git@github.com:Proteus-tech/deploy.git')
        self.assertEqual('git', user)
        self.assertEqual('github.com', host)
        self.assertEqual('Proteus-tech/deploy.git', path)

    def test_split_private_git_url_inside_server(self):
        user, host, path = split_private_git_url('ssh://git@zeppelin:222/home/git/playable_admin_service')
        self.assertEqual('git', user)
        self.assertEqual('zeppelin.proteus-tech.com', host)
        self.assertEqual('playable_admin_service', path)


        

