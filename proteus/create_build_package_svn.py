#!/usr/bin/env python

from profab.role import Role
from proteus import buildbot
from fabric.context_managers import cd, prefix
from fabric.api import local, run, sudo
from proteus import svn_checkout

def checkout_deploy_code(server, project_name, deploy_url, branch="develop"):
    project_base_folder = "/home/www-data/%s" % (project_name)
    deploy_base_folder = "deploy"
    with cd(project_base_folder):
        sudo("git clone -q %s %s" % (deploy_url, deploy_base_folder), user="www-data")
        with cd(deploy_base_folder):
            sudo("git checkout -b %s" % (branch), user="www-data")
            sudo("git pull origin %s" % (branch), user="www-data")
            sudo("git checkout %s" % (branch), user="www-data")

def create_virtenv(server, project_name):
    deploy_base = "/home/www-data/%s/deploy" % (project_name)
    project_base = "/home/www-data/%s" % (project_name)
    current_folder = "%s/current" % (project_base)
    with cd(current_folder):
        sudo("virtualenv --no-site-packages virtualenv", user="www-data")
        with prefix("source virtualenv/bin/activate"):
            sudo("pip install -r service/setup/requirements.txt", user="www-data")
            #sudo("pip install -r current/service/setup/server.pip", user="www-data")
            sudo("virtualenv --relocatable virtualenv", user="www-data")    

#def get_machine_spec(server):
#    ubuntu_version = run('lsb_release', '-cs').strip()
#    bits = run('uname', '-m').strip()
#    return (ubuntu_version, bits)
#
#def export_code_from_svn(server, svn_url):
#    svn_out = sudo("""svn log -l 1 --non-interactive --no-auth-cache
#        --trust-server-cert --username www-data --password 'www-d@t@!@#' %s
#        """ % (svn_url), user="www-data")
#    svn_rev = long(svn_out.split('\n')[1].split(' ')[0][1:])
#    ubuntu_version, bits = get_machine_spec(server)
#    return "%s.%s.%s.%s.tar.bz2" % (project_name, svn_rev, ubuntu_version, bits)
#
#def collect_static(server, project_name):
#    project_base = "/home/www-data/%s" % (project_name)
#    log_folder = "%s/logs" % (project_base)
#    with cd(project_base):
#        sudo("mkdir -p logs",user="www-data")
#        with prefix("source virtenv/bin/activate"):
#            sudo("service/manage.py collectstatic --noinput", user="www-data") 
#
#def create_tar_file(server, project_name, tar_filename):
#    project_base = "/home/www-data/%s" % (project_name)
#    current_revision_project = "%s/current" % (project_name)
#    with cd(current_revision_project):
#        sudo("tar cfa %s service static virtenv" % (tar_filename), user='www-data')
#
#def upload_tar_file(server, client_name, project_name):
#    pass
     

class Configure(Role):
    """
    Prerequesties - code should be in working directory.
    """
    def configure(self, server):
        svn_url = self.parameter
        project_name = svn_checkout.root_folder(svn_url)
        git_url = "git://github.com/Proteus-tech/deploy.git"

        checkout_deploy_code(server, project_name, git_url, branch="feature/PINFR241_siraset") 
        create_virtenv(server, project_name)
