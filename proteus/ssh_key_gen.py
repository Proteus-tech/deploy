from profab.role import Role
from fabric.contrib.files import exists
from fabric.operations import sudo

class AddRole(Role):
    """
    do ssh-keygen on server if key does not exist
    """
    def configure(self, server):
        if not exists("/home/www-data/.ssh/"):
            sudo("mkdir /home/www-data/.ssh/", user='www-data')
        if not exists('/home/www-data/.ssh/id_rsa'):
            sudo("ssh-keygen -b 4096 -f /home/www-data/.ssh/id_rsa -N ''", user='www-data')

