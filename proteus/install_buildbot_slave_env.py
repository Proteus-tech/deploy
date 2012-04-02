from fabric.context_managers import prefix
from fabric.operations import run, sudo
from profab.role import Role

def install_buildbot_slave_env(server, virtenv_path):
    sudo('easy_install pip')
    sudo('easy_install virtualenv')
    sudo("virtualenv --no-site-packages %s" % (virtenv_path), user="www-data")
    with prefix("source %s/bin/activate" % (virtenv_path)):
        sudo("pip install buildbot-slave==0.8.6", user="www-data")
 
class Configure(Role):
    """
    Create Buildbot Slave environment with parameter "virtual_env_full_path"
    """
    packages = [ 'build-essential'
        , 'python-dev'
        , 'python-setuptools'
    ]

    def configure(self, server):
        virtenv_path = self.parameter 
        install_buildbot_slave_env(server, virtenv_path)

