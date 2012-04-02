from fabric.api import settings
from fabric.operations import run, sudo
from profab.role import Role

def authorize_key(server, remote_host):
    public_key = sudo("cat /home/www-data/.ssh/id_rsa.pub", user='www-data')
    with settings(host_string=remote_host):
        authorized_keys = run('cat ~/.ssh/authorized_keys')
        if not public_key in authorized_keys:
            run('echo "%s" >> ~/.ssh/authorized_keys' % public_key)

class Configure(Role):
    def configure(self, server):
        '''
        add public key from of EC2 host to the remote host if not exist
        '''
        authorize_key(server, self.parameter)
