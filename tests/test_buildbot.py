from mock import Mock, patch
from unittest import TestCase
import buildbot

class TestStart(TestCase):
    def setUp(self):
        self.patch_start = patch('simpleserver.start')
        self.mock_start = self.patch_start.start() 
        self.mock_start.return_value = server = Mock()
        server.get_role_adders = self.mock_adders = Mock()

    def tearDown(self):
        self.patch_start.stop()

    def test_simple_start(self):
        # Arrange
        client = 'bmf'
        project = 'fluffy'
        repository = 'git://github.com/juacompe/fluffy.git'
        # Act
        buildbot.start(client, project, repository)
        # Assert
        self.mock_start.assert_called_once_with('bmf')
        params = ('proteus.buildbot','fluffy,git://github.com/juacompe/fluffy.git')
        self.mock_adders.assert_called_once_with(params)

    def test_start_with_optional_parameters(self):
        # Arrange
        client = 'bmf'
        project = 'fluffy'
        repository = 'git://github.com/juacompe/fluffy.git'
        bits = 32
        region = 'us-west-2'
        ami = 'ami-4d5'
        # Act
        buildbot.start(client, project, repository, bits, region, ami)
        # Assert
        self.mock_start.assert_called_once_with('bmf', 32, 'us-west-2', 'ami-4d5')
        params = ('proteus.buildbot','fluffy,git://github.com/juacompe/fluffy.git')
        self.mock_adders.assert_called_once_with(params)

class TestSetup(TestCase):
    def setUp(self):
        self.patch_connect = patch('profab.server.Server.connect')
        self.mock_connect = self.patch_connect.start()
        self.mock_connect.return_value = server = Mock()
        server.get_role_adders = self.mock_adders = Mock()

    def tearDown(self):
        self.patch_connect.stop()
    
    def test_simple_setup(self):
        # Arrange
        client = 'bmf'
        ec2_host = 'ec2-50-18-236-118.us-west-1.compute.amazonaws.com' 
        project_name = 'fluffy'
        repository = 'git://github.com/juacompe/fluffy.git'
        # Act
        buildbot.setup(client, ec2_host, project_name, repository)
        # Assert
        self.mock_connect.assert_called_once_with(client=client, hostname=ec2_host)
        params = ('proteus.buildbot','fluffy,git://github.com/juacompe/fluffy.git')
        self.mock_adders.assert_called_once_with(params)
        
