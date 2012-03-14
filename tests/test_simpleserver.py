from mock import Mock, patch
from unittest import TestCase
import simpleserver

class TestStart(TestCase):
    def setUp(self):
        self.patch_start = patch('profab.server.Server.start')
        self.mock_start = self.patch_start.start()

    def tearDown(self):
        self.patch_start.stop()
    
    def test_simple_start(self):
        # Arrange
        client = 'bmf'
        # Act
        simpleserver.start(client)
        # Assert
        self.mock_start.assert_called_once_with('bmf'
            , ('security_group', 'ssh')
            , ('security_group', 'http')
            , ('postgres', None)
            , ('wsgi', None)
            , ('bits', '64')
            , ('region', 'us-west-1')
            , ('size', 't1.micro')
            , ('ami', 'ami-4d580408')
        )

    def test_start_with_parameters(self):
        # Arrange
        client = 'bmf'
        bits = '32'
        region = 'ap-south'
        size = 'm1.small'
        ami = 'ami-4d'
        # Act
        simpleserver.start(client, bits, region, size, ami)
        # Assert
        self.mock_start.assert_called_once_with('bmf'
            , ('security_group', 'ssh')
            , ('security_group', 'http')
            , ('postgres', None)
            , ('wsgi', None)
            , ('bits', '32')
            , ('region', 'ap-south')
            , ('size', 'm1.small')
            , ('ami', 'ami-4d')
        )

        
