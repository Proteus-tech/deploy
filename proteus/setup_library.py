from fabric.context_managers import prefix
from fabric.operations import run, sudo
from fabric.api import cd
from profab.role import Role

class Configure(Role):
    """
    Install packages from "project_root_path"
    """
    def configure(self, server):
        project_root_path = self.parameter
        with cd(project_root_path):
            if exists('setup/require_libs.txt'):
                list_pkg = run('cat setup/require_libs.txt')
                # This split should be work for linux
                pkgs = list_pkg.split('\r\n')
                for pkg in pkgs:
                    sudo('apt-get install -y %s' % (pkg))
            else:
                print 'setup/require_libs.txt not found!'

                     
