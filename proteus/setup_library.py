from fabric.operations import sudo
from fabric.api import cd, run
from fabric.contrib.files import exists
from profab.role import Role
from profab import _logger


def setup_library(server, requirelibs_path):
    if exists(requirelibs_path):
        list_pkg = run('cat %s' % (requirelibs_path))
        # This split should be work for linux
        pkgs = list_pkg.split('\r\n')
        for pkg in pkgs:
            if pkg != '':
                sudo('apt-get install -y %s' % (pkg))
    else:
        info = '%s not found!' % (requirelibs_path)
        _logger.info(info)
        print info

   

class Configure(Role):
    """
    Install packages from full path point to requirelibs.txt

    - require
        path to /setup/requirelibs.txt
    """
    def configure(self, server):
        setup_library(server, self.parameter)
                     
