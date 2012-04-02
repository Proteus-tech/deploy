from fabric.operations import sudo
from fabric.api import cd, run
from fabric.contrib.files import exists
from profab.role import Role
from profab import _logger

class Configure(Role):
    """
    Install packages from "project_root_path", e.g. '/home/www-data/Buildbot/<project-name>'

    - require
        Folder '/home/www-data/Buildbot/<project-name>/src' must valid before use this role and
        src folder contains project code.
    """
    def configure(self, server):
        project_root_path = self.parameter
        lib_file_path = 'src/setup/requirelibs.txt'
        with cd(project_root_path):
            if exists(lib_file_path):
                list_pkg = run('cat %s' % (lib_file_path))
                # This split should be work for linux
                pkgs = list_pkg.split('\r\n')
                for pkg in pkgs:
                    if pkg != '':
                        sudo('apt-get install -y %s' % (pkg))
            else:
                info = '%s/%s not found!' % (project_root_path, lib_file_path)
                _logger.info(info)
                print info

                 


                     
