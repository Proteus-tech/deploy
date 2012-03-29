from fabric.operations import sudo
from fabric.api import cd
from fabric.contrib.files import exists
from profab.role import Role
from profab import _logger

class Configure(Role):
    """
    Install packages from "project_root_path"
    e.g.
        project_root_path = '/home/www-data/project-name'
    """
    def configure(self, server):
        project_root_path = self.parameter
        with cd(project_root_path):
            if exists('setup/requirelibs.txt'):
                list_pkg = run('cat setup/requirelibs.txt')
                # This split should be work for linux
                pkgs = list_pkg.split('\r\n')
                for pkg in pkgs:
                    if pkg != '':
                        sudo('apt-get install -y %s' % (pkg))
            else:
                _logger.info('setup/requirelibs.txt not found!')


                     
