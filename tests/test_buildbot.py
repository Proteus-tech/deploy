from mock import Mock, patch
from unittest import TestCase
import buildbot

class TestStart(TestCase):
    def setUp(self):
        self.master_src_path = '/home/www-data/Buildbot/%s'
        self.patch_start = patch('simpleserver.start')
        self.mock_start = self.patch_start.start() 
        self.mock_start.return_value = server = Mock()
        server.get_role_adders = self.mock_adders = Mock()

    def tearDown(self):
        self.patch_start.stop()

    def test_simple_start(self):
        # Arrange
        client = 'proteus'
        project = 'fluffy'
        repository = 'git://github.com/juacompe/fluffy.git'
        # Act
        buildbot.start(client, project, repository)
        # Assert
        self.mock_start.assert_called_once_with('proteus')
        checkout_parameters = '%s,%s' % (self.master_src_path % project, repository)
        master_cfg_params = '/home/www-data/Buildbot/fluffy/src/buildbot/master.cfg' \
            ',/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg'
        complete_params = '/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg' \
            ',git://github.com/juacompe/fluffy.git'
        check_config_params = '/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg' \
            ',/home/www-data/Buildbot/fluffy/virtenv-master'
        params = [('proteus.www_home','')
            , ('proteus.install_buildbot_master_env','/home/www-data/Buildbot/fluffy/virtenv-master')
            , ('proteus.setup_buildbot_master','fluffy')
            , ('proteus.git_checkout', checkout_parameters)
            , ('proteus.create_symlink', master_cfg_params)
            , ('proteus.complete_master_config', complete_params)
            , ('proteus.install_buildbot_slave_env','/home/www-data/Buildbot/fluffy/virtenv-slave')
            , ('proteus.setup_buildbot_slave','fluffy,slave1,localhost')
            , ('proteus.check_config',check_config_params)
            , ('proteus.buildbot' ,'fluffy,git://github.com/juacompe/fluffy.git')
            , ('smarthost',None)]
        self.mock_adders.assert_called_once_with(*params)

    def test_start_with_optional_parameters(self):
        # Arrange
        client = 'proteus'
        project = 'fluffy'
        repository = 'git://github.com/juacompe/fluffy.git'
        privacy = 'public'
        bits = '32'
        region = 'us-west-2'
        ami = 'ami-4d5'
        # Act
        buildbot.start(client, project, repository, privacy, bits, region, ami)
        # Assert
        checkout_parameters = '%s,%s' % (self.master_src_path % project, repository)
        master_cfg_params = '/home/www-data/Buildbot/fluffy/src/buildbot/master.cfg' \
            ',/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg'
        complete_params = '/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg' \
            ',git://github.com/juacompe/fluffy.git'
        check_config_params = '/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg' \
            ',/home/www-data/Buildbot/fluffy/virtenv-master'
        self.mock_start.assert_called_once_with('proteus', '32', 'us-west-2', 'ami-4d5')
        params = [('proteus.www_home','')
            , ('proteus.install_buildbot_master_env','/home/www-data/Buildbot/fluffy/virtenv-master')
            , ('proteus.setup_buildbot_master','fluffy')
            , ('proteus.git_checkout', checkout_parameters)
            , ('proteus.create_symlink', master_cfg_params)
            , ('proteus.complete_master_config', complete_params)
            , ('proteus.install_buildbot_slave_env','/home/www-data/Buildbot/fluffy/virtenv-slave')
            , ('proteus.setup_buildbot_slave','fluffy,slave1,localhost')
            , ('proteus.check_config',check_config_params)
            , ('proteus.buildbot','fluffy,git://github.com/juacompe/fluffy.git')
            , ('smarthost',None)]
        self.mock_adders.assert_called_once_with(*params)


class TestSetup(TestCase):
    def setUp(self):
        self.master_src_path = '/home/www-data/Buildbot/%s'
        self.patch_connect = patch('profab.server.Server.connect')
        self.mock_connect = self.patch_connect.start()
        self.mock_connect.return_value = server = Mock()
        server.get_role_adders = self.mock_adders = Mock()

    def tearDown(self):
        self.patch_connect.stop()
    
    def test_setup_with_public_git(self):
        # Arrange
        client = 'proteus'
        ec2_host = 'ec2-50-18-236-118.us-west-1.compute.amazonaws.com' 
        project = 'fluffy'
        repository = 'git://github.com/juacompe/fluffy.git'
        # Act
        buildbot.setup(client, ec2_host, project, repository)
        # Assert
        self.mock_connect.assert_called_once_with(client=client, hostname=ec2_host)
        checkout_parameters = '%s,%s' % (self.master_src_path % project, repository)
        master_cfg_params = '/home/www-data/Buildbot/fluffy/src/buildbot/master.cfg' \
            ',/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg'
        complete_params = '/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg' \
            ',git://github.com/juacompe/fluffy.git'
        check_config_params = '/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg' \
            ',/home/www-data/Buildbot/fluffy/virtenv-master'
        params = [('proteus.www_home','')
            , ('proteus.install_buildbot_master_env','/home/www-data/Buildbot/fluffy/virtenv-master')
            , ('proteus.setup_buildbot_master','fluffy')
            , ('proteus.git_checkout', checkout_parameters)
            , ('proteus.create_symlink', master_cfg_params)
            , ('proteus.complete_master_config', complete_params)
            , ('proteus.install_buildbot_slave_env','/home/www-data/Buildbot/fluffy/virtenv-slave')
            , ('proteus.setup_buildbot_slave','fluffy,slave1,localhost')
            , ('proteus.check_config',check_config_params)
            , ('proteus.buildbot','fluffy,git://github.com/juacompe/fluffy.git')
            , ('smarthost',None) ]
        self.mock_adders.assert_called_once_with(*params)
        
    def test_setup_with_private_git(self):
        client = 'proteus'
        ec2_host = 'ec2-50-18-236-118.us-west-1.compute.amazonaws.com' 
        project = 'fluffy'
        repository = 'git@git.private.net:/home/git/project/projectlib.git'
        privacy = 'private'
        # Act
        buildbot.setup(client, ec2_host, project, repository, privacy)
        # Assert
        self.mock_connect.assert_called_once_with(client=client, hostname=ec2_host)
        checkout_parameters = '%s,%s' % (self.master_src_path % project, repository)
        master_cfg_params = '/home/www-data/Buildbot/fluffy/src/buildbot/master.cfg' \
            ',/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg'
        complete_params = '/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg,%s' % repository
        check_config_params = '/home/www-data/Buildbot/fluffy/buildbot-master/master.cfg' \
        ',/home/www-data/Buildbot/fluffy/virtenv-master'
        params = [('proteus.www_home','')
            , ('proteus.ssh_key_gen', '')
            , ('proteus.authorize_key', 'git@git.private.net:/home/git/project/projectlib.git')
            , ('proteus.trust_host', 'git.private.net')
            , ('proteus.install_buildbot_master_env','/home/www-data/Buildbot/fluffy/virtenv-master')
            , ('proteus.setup_buildbot_master','fluffy')
            , ('proteus.git_checkout', checkout_parameters)
            , ('proteus.create_symlink', master_cfg_params)
            , ('proteus.complete_master_config', complete_params)
            , ('proteus.install_buildbot_slave_env','/home/www-data/Buildbot/fluffy/virtenv-slave')
            , ('proteus.setup_buildbot_slave','fluffy,slave1,localhost')
            , ('proteus.check_config',check_config_params)
            , ('proteus.buildbot','fluffy,git@git.private.net:/home/git/project/projectlib.git')
            , ('smarthost', None)
        ]
        self.mock_adders.assert_called_once_with(*params)
 

class TestSplitPrivateGitUrl(TestCase):
    def test_ssh_url(self):
        url = 'git@git.private.net:/home/git/project/projectlib.git'
        user, host, path = buildbot.split_private_git_url(url)
        self.assertEqual('git', user)
        self.assertEqual('git.private.net', host)
        self.assertEqual('/home/git/project/projectlib.git', path)

