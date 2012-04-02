from fabric.operations import sudo
from profab.role import Role

def www_home(server):
    sudo("/etc/init.d/apache2 stop")
    sudo("usermod --home /home/www-data --shell /bin/bash www-data")
    sudo("/etc/init.d/apache2 start")   

class AddRole(Role):
    def configure(self, server):
        '''
        self home of www-data to /home/www-data/ and specify bash as default shell
        '''
        www_home(server)
