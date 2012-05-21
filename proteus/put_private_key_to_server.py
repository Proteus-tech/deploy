from fabric.api import local, settings
from fabric.contrib.files import exists
from fabric.operations import run, sudo
from profab.role import Role
from proteus.authorize_key import authorize_key
from proteus import buildbot

def put_private_key_to_server(server, current_user, remote_host):
    current_home = '/home/%s' % current_user
    private_key = local('sudo cat %s/.ssh/id_rsa' %current_home)
    with settings(host_string=remote_host):
        if not exists('%s/.ssh/' % current_home):
            sudo('mkdir %s/.ssh/' % current_home, user=current_user)
        if not exists('%s/.ssh/id_rsa' % current_home):
            sudo('echo "%s" >> %s/.ssh/id_rsa' % (private_key, current_home), user=current_user)
            sudo('chmod 600 %s/.ssh/id_rsa' % current_home, user=current_user)


class Configure(Role):
    """
    Role to put private key to target server
    """
    def configure(self, server):
        if ',' not in self.parameter:
            remote_host = self.parameter
            current_user = 'www-data'
        else:
            remote_host, current_user = buildbot.splitter(self.parameter)
        
        put_private_key_to_server(server, current_user, remote_host)

