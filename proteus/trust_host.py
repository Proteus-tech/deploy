from fabric.contrib.files import exists
from fabric.operations import sudo
from profab.role import Role

class Configure(Role):
    def configure(self, server):
        '''
        config ssh to trust (skip host checking) of the remote_host
        '''
        remote_host = self.parameter
        if not exists("/home/www-data/.ssh/"):
            sudo("mkdir /home/www-data/.ssh/", user='www-data')
        if not exists('/home/www-data/.ssh/config'):
            sudo("touch /home/www-data/.ssh/config", user='www-data')
        content = ['Host %s' % remote_host, '   StrictHostKeyChecking no']
        content = '\n'.join(content)
        sudo('echo "%s" >> /home/www-data/.ssh/config' % content, user='www-data')

