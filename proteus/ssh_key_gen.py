from profab.role import Role
from fabric.contrib.files import exists
from fabric.operations import sudo

def ssh_key_gen(server):
    """
    do ssh-keygen on server if key does not exist
    """
    if not exists("/home/www-data/.ssh/"):
        sudo("mkdir /home/www-data/.ssh/", user='www-data')
    if not exists('/home/www-data/.ssh/id_rsa'):
        sudo("ssh-keygen -b 4096 -f /home/www-data/.ssh/id_rsa -N ''", user='www-data')


class AddRole(Role):
    def configure(self, server):
        ssh_key_gen(server)
