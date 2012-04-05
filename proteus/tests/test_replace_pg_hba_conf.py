import mock 
from proteus.replace_pg_hba_conf import AddRole
from unittest import TestCase


class TestReplacePgHbaConf(TestCase):
    """Test Replace to pg_hba.conf.
    """
    @mock.patch('proteus.replace_pg_hba_conf.sudo')
    @mock.patch('proteus.replace_pg_hba_conf.exists')
    @mock.patch('proteus.replace_pg_hba_conf.sed')

    def test_select_postgres_v9_1(self, sed, exist, sudo):
        # Arrange
        role = AddRole()
        server = mock.Mock()
        pg_hba_path = '/etc/postgresql/9.1'
        def side_effect(arg):
            output = {
                '/etc/postgresql/9.1' : True,
                '/etc/postgresql/8.4' : False,
            }
            return output[arg]
        exist.side_effect = side_effect 
        # Act
        role.configure(server)
        # Assert
        first_call = sed.call_args_list[0]
        expected = mock.call('%s/main/pg_hba.conf' % pg_hba_path
            , '# If you want to allow non-local connections, you need to add more'
            , 'local   all all             trust'
            , use_sudo=True)
        self.assertEqual(expected, first_call)
        second_call = sed.call_args_list[1]
        expected = mock.call('%s/main/pg_hba.conf' % pg_hba_path
            , '# "host" records. In that case you will also need to make PostgreSQL listen'
            , 'host    all all     127.0.0.1/32    md5'
            , use_sudo=True)
        self.assertEqual(expected, second_call)

        sudo.assert_called_once_with('/etc/init.d/postgresql restart')
    
    @mock.patch('proteus.replace_pg_hba_conf.sudo')
    @mock.patch('proteus.replace_pg_hba_conf.exists')
    @mock.patch('proteus.replace_pg_hba_conf.sed')

    def test_select_postgres_v8_4(self, sed, exist, sudo):
        # Arrange
        role = AddRole()
        server = mock.Mock()
        pg_hba_path = '/etc/postgresql/8.4'
        def side_effect(arg):
            output = {
                '/etc/postgresql/9.1' : False,
                '/etc/postgresql/8.4' : True,
            }
            return output[arg]
        exist.side_effect = side_effect 
        # Act
        role.configure(server)
        # Assert
        first_call = sed.call_args_list[0]
        expected = mock.call('%s/main/pg_hba.conf' % pg_hba_path
            , '# If you want to allow non-local connections, you need to add more'
            , 'local   all all             trust'
            , use_sudo=True)
        self.assertEqual(expected, first_call)
        second_call = sed.call_args_list[1]
        expected = mock.call('%s/main/pg_hba.conf' % pg_hba_path
            , '# "host" records. In that case you will also need to make PostgreSQL listen'
            , 'host    all all     127.0.0.1/32    md5'
            , use_sudo=True)
        self.assertEqual(expected, second_call)

        sudo.assert_called_once_with('/etc/init.d/postgresql restart')

    @mock.patch('proteus.replace_pg_hba_conf.sudo')
    @mock.patch('proteus.replace_pg_hba_conf.exists')
    @mock.patch('proteus.replace_pg_hba_conf.sed')

    def test_select_postgres_not_support(self, sed, exist, sudo):
        # Arrange
        role = AddRole()
        server = mock.Mock()
        def side_effect(arg):
            output = {
                '/etc/postgresql/9.1' : False,
                '/etc/postgresql/8.4' : False,
            }
            return output[arg]
        exist.side_effect = side_effect 
        # Assert
        self.assertRaises(Exception, role.configure, server)
        

