#!/usr/bin/env python

import os

from fabric.contrib.files import upload_template, exists
from profab.role import Role
from proteus import buildbot
from fabric.context_managers import cd, prefix
from fabric.api import local, run, sudo
from profab import _logger
from proteus import svn_checkout
from proteus import upload_packages

def checkout_deploy_sourcecode(server, project_name, deploy_url, branch="develop"):
    project_base_folder = "/home/www-data/%s" % (project_name)
    deploy_base_folder = "deploy"
    with cd(project_base_folder):
        sudo("git clone -q %s %s" % (deploy_url, deploy_base_folder), user="www-data")
        with cd(deploy_base_folder):
            sudo("git checkout -b %s" % (branch), user="www-data")
            sudo("git pull origin %s" % (branch), user="www-data")
            sudo("git checkout %s" % (branch), user="www-data")

def create_virtenv(server, project_name):
    sudo("easy_install virtualenv")
    project_base_dir = "/home/www-data/%s" % (project_name)
    current_dir = "%s/current" % (project_base_dir)
    with cd(current_dir):
        sudo("virtualenv --no-site-packages virtualenv", user="www-data")
        with prefix("source virtualenv/bin/activate"):
            sudo("pip install -r service/setup/requirements.txt", user="www-data")
            #sudo("pip install -r current/service/setup/server.pip", user="www-data")
            sudo("virtualenv --relocatable virtualenv", user="www-data")    

def _get_project_name(svn_url):
    if svn_url.endswith('/'):
        svn_url = svn_url.rstrip('/')
        return svn_url.split('/')[-2]
    else:
        return None

def _get_machine_spec(server):
    ubuntu_version = run('lsb_release', '-cs').strip()
    bits = run('uname', '-m').strip()
    return (ubuntu_version, bits)

def get_build_package_name(server, svn_url):
    svn_out = sudo("""svn log -l 1 --non-interactive --no-auth-cache
        --trust-server-cert --username www-data --password 'www-d@t@!@#' %s
        """ % (svn_url), user="www-data")
    svn_rev = long(svn_out.split('\n')[1].split(' ')[0][1:])
    ubuntu_version, bits = get_machine_spec(server)
    project_name = _get_project_name(svn_url)
    return "%s.%s.%s.%s.tar.bz2" % (project_name, svn_rev, ubuntu_version, bits)

def collect_static(server, project_name):
    project_base_dir = "/home/www-data/%s" % (project_name)
    with cd(project_base_dir):
        sudo("mkdir -p logs",user="www-data")
        with prefix("source virtualenv/bin/activate"):
            sudo("python service/manage.py collectstatic --noinput", user="www-data")

def create_tar_file(server, project_name, tarfile_name):
    project_base_dir = "/home/www-data/%s" % (project_name)
    current_dir = "%s/current" % (project_base_dir)
    with cd(current_dir):
        sudo("tar cfa %s service static virtenv" % (tarfile_name), user='www-data')
        path_to_tarfile = '%s/%s' % (current_dir, tarfile_name)
        return path_to_tarfile



#def setup_s3tool_for_remote_machine(server):
#    '''
#    upload s3cfg to remote machine
#    '''
#    config_dir = "templates/s3cfg"
#    if exists(config_dir):
#        _logger.info('found s3cmd configuration file at %s ', config_dir)
#        upload_template(config_dir, ".s3cfg")
#        run('chmod a+r .s3cfg')
#
#
#def s3cmd_upload_build_pkg(server, path_to_tarfile, bucket_name):
#    keyname = os.path.split(path_to_tarfile.rstrip('/'))[1]
#    sudo("s3cmd put %s s3://%s/%s" % (bucket_name, keyname))


class Configure(Role):
    """
    Create build package, then upload to s2
    - usage
        --proteus.create_build_package_svn git_url,svn_url
        * git_url : deploy git 
            should be "git://github.com/Proteus-tech/deploy.git" 
        ** svn_url : project svn
    """
    packages = [
        'python-setuptools',
        'git-core',
        'subversion',
        's3cmd'
    ]
    def configure(self, server):
        git_url, svn_url = buildbot.splitter(self.parameter)

        # get project name from svn_url
        project_name = svn_checkout.root_folder(svn_url)

        # checkout deploy code to use in host machine
        # for using role
        checkout_deploy_sourcecode(server, project_name, git_url)

        # create virtual environment from requirements.txt
        create_virtenv(server, project_name)

        # do collectstatic
        collect_static(server, project_name)

        # just get only build package name
        bpkg_name = get_build_package_name(server, svn_url)

        # create tar file
        path_to_tarfile = create_tar_file(server, project_name, bpkg_name)

        # setup s3cmd tools
        bucket_name = 'build-pkg-%s' % (project_name)
        upload_packages.upload_package(server, bucket_name , path_to_tarfile)








