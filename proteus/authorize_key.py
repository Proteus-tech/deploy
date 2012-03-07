from fabric.api import settings
from fabric.operations import run, sudo
from profab.role import Role

class Configure(Role):
    def configure(self, server):
        '''
        add public key from of EC2 host to the remote host if not exist
        '''
        public_key = sudo("cat /home/www-data/.ssh/id_rsa.pub", user='www-data')
        remote_host = self.parameter 
        with settings(host_string=remote_host):
            authorized_keys = run('cat ~/.ssh/authorized_keys')
            if not public_key in authorized_keys:
                run('echo "%s" >> ~/.ssh/authorized_keys' % public_key)

