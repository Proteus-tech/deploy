from fabric.contrib.files import exists
from fabric.operations import sudo
from profab.role import Role

def trust_host(server, remote_host):
    if not exists("/home/www-data/.ssh/"):
        sudo("mkdir /home/www-data/.ssh/", user='www-data')
    if not exists('/home/www-data/.ssh/config'):
        sudo("touch /home/www-data/.ssh/config", user='www-data')
    content = ['Host %s' % remote_host, '   StrictHostKeyChecking no']
    content = '\n'.join(content)
    sudo('echo "%s" >> /home/www-data/.ssh/config' % content, user='www-data')


class Configure(Role):
    def configure(self, server):
        '''
        config ssh to trust (skip host checking) of the remote_host
        '''
        trust_host(server, self.parameter)
