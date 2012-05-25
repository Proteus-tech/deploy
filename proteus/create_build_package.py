#!/usr/bin/env python
from profab.role import Role
#from profab.state import env
#from fabric.decorators import with_settings
from proteus import buildbot
from fabric.api import local, run
from proteus import upload_tar_to_s3

# should relocate to buildbot.py
def create_virtenv(server, project_name):
    with cd(project_name):
        sudo("scripts/virtenv", user="www-data")

def get_tar_name(server, project_name, svn_rev):
    ubuntu_version = run('lsb_release', '-cs').strip()
    bits = run('uname', '-m').strip()
    tarfile = "%s.%s.%s.%s.tar.bz2" % (project_name, svn_rev, ubuntu_version, bits)
    return tarfile    

def export_code_from_svn(server, svn_url):
    svn_out = sudo("""svn log -l 1 --non-interactive --no-auth-cache
        --trust-server-cert --username www-data --password 'www-d@t@!@#' %s
        """ % (svn_url), user="www-data")
    svn_rev = long(svn_out.split('\n')[1].split(' ')[0][1:])
    
    return get_tar_name(server, project_name, svn_url)

def create_build_package(server):
    '''
    1. create virtual env
    2. pip install python lib from requirements.txt
    3. collectstatic
    4. runtest
    5. remove pyc
    6. tar create tar
    7. rename tar file
    '''
    pass
    

class Configure(Role):
    def configure(self, server):
        pass

