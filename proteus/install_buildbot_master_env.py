from fabric.context_managers import prefix
from fabric.operations import run, sudo
from profab.role import Role

class Configure(Role):
    """
    Create Buildbot Master environment with parameter "virtual_env_full_path"
    """
    packages = [ 'build-essential'
        , 'python-dev'
        , 'python-setuptools'
    ]

    def configure(self, server):
        sudo('easy_install pip')
        sudo('easy_install virtualenv')
        virtenv_path = self.parameter 
        sudo("virtualenv --no-site-packages %s" % (virtenv_path), user="www-data")
        with prefix("source %s/bin/activate" % (virtenv_path)):
            sudo("pip install buildbot==0.8.4", user="www-data")
 
