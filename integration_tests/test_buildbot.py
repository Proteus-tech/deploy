#!usr/bin/python
from fabric.api import settings
from fabric.context_managers import prefix
from fabric.operations import sudo, local, run
from fabric.contrib.files import exists
from os.path import abspath
from profab.server import Server 
from subprocess import call
from unittest import TestCase
import sys
import os

from proteus.install_buildbot_slave_env import install_buildbot_slave_env

class TestBuildbot(TestCase):

    @classmethod
    def create_simple_server(cls):
        """
        Simulate bin/start-simple-server script by create a new instance using
        roles as simple server script. 
        """
        role_tuple_list = [
              ('security_group','ssh')
            , ('security_group','http')
            , ('wsgi','')
            , ('bits','64')
            , ('region','us-west-1')
            , ('size','t1.micro')
            , ('ami','ami-4d580408')
        ]
        cls.server = Server.start('proteus', *role_tuple_list)
        assert cls.server, 'Server should be connected'

    @classmethod
    def connect_to_server(cls, ec2_host):
        cls.server = Server.connect('proteus', ec2_host)

    @classmethod
    def setUpClass(cls):

        # clean previous step
        os.system('rm -rf /tmp/proteus-deploy-int/')
        os.system('rm -rf /tmp/easy_install-*')

        tmp_path = os.getcwd()
        os.chdir('..')
        os.system('virtualenv /tmp/proteus-deploy-int')
        activate_this = '/tmp/proteus-deploy-int/bin/activate_this.py'
        execfile(activate_this, dict(__file__=activate_this))
        os.system('python setup.py install')
        os.system('pip install nose')
        os.chdir(tmp_path)

        cls.create_simple_server()

    @classmethod
    def tearDownClass(cls):
        '''
        delete environment and unuse folder
        terminate server
        '''
        
        cls.server.stop()
        cls.server.terminate()

        #self.delete_remote_buildbot_folder()
        #self.delete_local_tmp_folder() 
        
        os.system('rm -rf /tmp/proteus-deploy-int/')
        os.system('rm -rf /tmp/easy_install-*')

        os.system('rm -rf ../build/ ../dist/ ../proteus_deploy.egg-info/')

    def setUp(self):
        self.ec2_host = self.server.instance.dns_name
        self.host_string = 'ubuntu@%s' % self.ec2_host

    def tearDown(self):
        self.delete_remote_buildbot_folder()
        #self.delete_tmp_folder()
        self.delete_remote_postgres_related()

    def delete_remote_buildbot_folder(self):
        with settings(host_string=self.host_string):
            sudo('rm -rf /home/www-data/Buildbot')

    def delete_local_tmp_folder(self):
        os.system('rm -rf /tmp/proteus-deploy-int/')
        os.system('rm -rf /tmp/easy_install-*')

    def delete_remote_postgres_related(self):
        with settings(host_string=self.host_string):
            check_result = sudo('''psql -a -c "select datname from pg_database"''', user='postgres')
            if 'hobby' in check_result:
                sudo('''psql -c "DROP DATABASE hobby;" ''', user='postgres')
            check_result = sudo('''psql -a -c "select usename from pg_user"''', user='postgres')
            if 'hobby' in check_result:
                sudo('''psql -c "DROP USER hobbyuser;" ''', user='postgres')

    ###  Scenario-1 : setting up buildbot master environment 
    def test_setup_buildbot_master_env(self):
        # Arrange
        master_virtual_env_path = '/home/www-data/Buildbot/hobby/virtenv-master'
        # Act
        # TODO call from script to test script too
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.install_buildbot_master_env'
            , master_virtual_env_path]) 
        #remote_function = _on_this_server(install_buildbot_master_env)
        #remote_function(self.server, master_virtual_env_path)
        # Assert
        with settings(host_string=self.host_string):
            activate = 'source %s/bin/activate' % master_virtual_env_path
            with prefix(activate):
                # test that environment can be activated
                output = sudo('env | grep virtenv-master')
                self.assertTrue('VIRTUAL_ENV=/home/www-data/Buildbot/hobby/virtenv-master' in output)
                # test that environment contains buildbot package
                output = sudo('pip freeze')
                self.assertTrue('buildbot' in output)

    ### Scenario-2 : create and setting for postgres database
    def test_create_pg_db(self):
        # Arrange
        slave_virtual_env_path = '/home/www-data/Buildbot/hobby/virtenv-slave'

        '''0.run role postgres
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , 'postgres']) 
        # Assert
        with settings(host_string=self.host_string):
            # test have postgresql in server
            output = sudo('ls /etc/')
            self.assertTrue('postgresql' in output)

        ''' 1.run role install_buildbot_slave_env
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.install_buildbot_slave_env'
            , slave_virtual_env_path]) 
        # Assert
        with settings(host_string=self.host_string):
            # test have slave env slave on server
            output = sudo('ls /home/www-data/Buildbot/hobby')
            self.assertTrue('virtenv-slave' in output)

        ''' 2.run role setup_buildbot_pg_slave
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.setup_buildbot_pg_slave'
            , '/home/www-data/Buildbot/hobby,slave-pg,localhost']) 
        # Assert
        with settings(host_string=self.host_string):
            # test directory is created
            output = sudo('ls /home/www-data/Buildbot/hobby/buildslave2')
            self.assertTrue('builder-pg' in output)
            # test file is changed
            output = sudo('cat /home/www-data/Buildbot/hobby/buildslave2/buildbot.tac')
            self.assertTrue("slavename = 'slave-pg'" in output)
            self.assertTrue("passwd = 'slave-pgpassword'" in output)
        
        ''' 3.run role git_checkout
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.git_checkout'
            , '/home/www-data/Buildbot/hobby/buildslave2/builder-pg,git://github.com/juacompe/hobby.git']) 
        # Assert
        with settings(host_string=self.host_string):
            # test directory is created
            output = sudo('ls /home/www-data/Buildbot/hobby/buildslave2/builder-pg')
            self.assertTrue('src' in output)
            output = sudo('ls /home/www-data/Buildbot/hobby/buildslave2/builder-pg/bin')
            self.assertTrue('update_master_config' in output)
        
        ''' 4.run role setup_library
        '''
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.setup_library'
            , '/home/www-data/Buildbot/hobby/buildslave2/builder-pg/src/setup/requirelibs.txt']) 
        # Assert
        with settings(host_string=self.host_string):
            # test package is installed
            output = sudo('aptitude search libpq-dev')
            self.assertTrue('i   libpq-dev' in output)
            output = sudo('aptitude search build-essential')
            self.assertTrue('i   build-essential' in output)
            output = sudo('aptitude search libpng-dev')
            self.assertTrue('v   libpng-dev' in output)
            output = sudo('aptitude search libjpeg-dev')
            self.assertTrue('v   libjpeg-dev' in output)
            output = sudo('aptitude search python-dev')
            self.assertTrue('i   python-dev' in output)
            output = sudo('aptitude search python-setuptools')
            self.assertTrue('i   python-setuptools' in output)

        ''' 5.run role setup_psycopg2_on_slave
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.setup_psycopg2_on_slave'
            , 'hobby,/home/www-data/Buildbot/hobby/buildslave2/builder-pg']) 
        # Assert
        with settings(host_string=self.host_string):
            # test have psycopg2 in server
            activate = 'source %s/bin/activate' % slave_virtual_env_path
            with prefix(activate):
                output = sudo('pip freeze')
                self.assertTrue('psycopg2' in output)
                
        '''7.run role replace_pg_hba_conf
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , 'proteus.replace_pg_hba_conf']) 
        # Assert
        with settings(host_string=self.host_string):
            # test pg_hba.conf is modified
            output = sudo('cat /etc/postgresql/8.4/main/pg_hba.conf')
            self.assertTrue('local   all all             trust' in output)
            self.assertTrue('host    all all     127.0.0.1/32    md5' in output)    
        
        ''' 8. run role create_pg_db'
        '''
        # Act
        call(['pf-server-role-add'
            , 'proteus'
            , self.ec2_host
            , '--proteus.create_pg_db'
            , 'hobby,git://github.com/juacompe/hobby.git']) 
        # Assert
        with settings(host_string=self.host_string):
            # test user is created
            output = run('psql -c "\l" -A')
            self.assertTrue('hobbyuser' in output)
            # test database is created
            self.assertTrue('hobby' in output)
            
    ### Scenario-3 : setting buildbot slave with postgres
    def test_setup_buildbot_pg_slave(self):
        ### try to get original pg_hba before postgres role dominate this test
        with settings(host_string=self.host_string):
            linux_codename = sudo('lsb_release -cs')
            if 'natty' in linux_codename:
                pg_version = '8.4'
            elif 'oneiric' in linux_codename:
                pg_version = '9.1'
            else:
                pg_version = '8.4'
            pg_hba_conf_bak_path = '/etc/postgresql/%s/main/pg_hba.conf.bak' % (pg_version)
            pg_hba_conf_path = '/etc/postgresql/%s/main/pg_hba.conf' % (pg_version)
            self.assertTrue(exists(pg_hba_conf_bak_path),msg='%s is not valid.' % (pg_hba_conf_bak_path))
            sudo('mv %s %s' % (pg_hba_conf_bak_path, pg_hba_conf_path)) 

        slave_virtual_env_path = '/home/www-data/Buildbot/hobby/virtenv-slave'

        local('''setup-pg-slave-on-server \
                proteus \
                %s \
                localhost \
                hobby \
                git://github.com/juacompe/hobby.git''' 
                % (self.ec2_host)
        )

        with settings(host_string=self.host_string):
            # check if postres was installed.
            output = sudo('aptitude search postgres')
            self.assertTrue('i   postgresql' in output)
            self.assertTrue('i A postgresql-' in output) 

            activate = 'source %s/bin/activate' % slave_virtual_env_path
            with prefix(activate):
                # check if virtenv-slave is valid.
                output = sudo('env | grep virtenv-slave')
                self.assertTrue('VIRTUAL_ENV=/home/www-data/Buildbot/hobby/virtenv-slave' in output)
                
                # check if buildbot-slave environment was installed.
                output = sudo('pip freeze')
                self.assertTrue('buildbot-slave' in output)

                # check if buildbot slave was installed and git check out work correctly.
                self.assertTrue(exists('/home/www-data/Buildbot/hobby/buildslave2/builder-pg/src'))

                # check if needed libraries were installed.
                output = sudo('aptitude search libpq-dev')
                self.assertTrue('i   libpq-dev' in output)
                output = sudo('aptitude search python-psycopg')
                self.assertTrue('i   python-psycopg' in output)
                
                # check if psycopg2 was already install in virtual-env.
                output = sudo('pip freeze')
                self.assertTrue('psycopg' in output)

#            # check if pg_hba.conf was modified correctly.
#            linux_codename = sudo('lsb_release -cs')
#            if 'natty' in linux_codename:
#                pg_version = '8.4'
#            elif 'oneiric' in linux_codename:
#                pg_version = '9.1'
#            else:
#                pg_version = '8.4'
            
#            pg_hba_conf_bak_path = '/etc/postgresql/%s/main/pg_hba.conf.bak' % (pg_version)
#            pg_hba_conf_path = '/etc/postgresql/%s/main/pg_hba.conf' % (pg_version)
#            if exists(pg_hba_conf_bak_path):
#                sudo('mv %s %s' % (pg_hba_conf_bak_path, pg_hba_conf_path)) 

            output = sudo('cat %s' % (pg_hba_conf_path))
            self.assertTrue('local   all all             trust' in output)
            self.assertTrue('host    all all     127.0.0.1/32    md5' in output)
                    
            # check if postgresdb was created correctly.
            output = sudo("psql -c '\l' -U postgres -A")
            self.assertTrue('hobby|hobbyuser' in output)
