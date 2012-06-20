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
        if not exists(deploy_base_folder):
            sudo("git clone -q %s %s" % (deploy_url, deploy_base_folder), user="www-data")
            with cd(deploy_base_folder):
                sudo("git checkout -b %s" % (branch), user="www-data")
                sudo("git pull origin %s" % (branch), user="www-data")
                sudo("git checkout %s" % (branch), user="www-data")

def checkout_deploy_sourcecode_on_local(server, project_name, deploy_git_url, branch="develop"):
    project_base_folder = "/home/www-data/Buildbot/%s" % (project_name)
    deploy_base_folder = '%s/deploy' % (project_base_folder)
    local("git clone -q %s %s" % (deploy_git_url,deploy_base_folder ))
    local("cd %s && git checkout -b %s" % (deploy_base_folder, branch))
    local("cd %s && git pull origin %s" % (deploy_base_folder, branch))
    local("cd %s && git checkout %s" % (deploy_base_folder, branch))

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
    project_name = None
    if svn_url.endswith('/'):
        project_name = svn_url.rstrip('/').split('/')[-2]
    else:
        project_name = svn_url.split('/')[-2]
    return project_name

def _get_machine_spec(server):
    ubuntu_version = run('lsb_release -cs').strip()
    bits = run('uname -m').strip()
    return (ubuntu_version, bits)

def get_build_package_name(server, svn_url):
    project_name = _get_project_name(svn_url)
    service_dir = "/home/www-data/%s/current/service" % (project_name)
    with cd(service_dir):
        svn_out = sudo(
            "svn log -l 1 "
            "--non-interactive "
            "--no-auth-cache "
            "--trust-server-cert "
            "--username www-data --password 'www-d@t@!@#' %s "
            % (svn_url), user="www-data")
        svn_rev = long(svn_out.split('\n')[1].split(' ')[0][1:])
        ubuntu_version, bits = _get_machine_spec(server)

        return "%s.%s.%s.%s.tar.bz2" % (project_name, svn_rev, ubuntu_version, bits)


def collect_static(server, project_name):
    project_base_dir = "/home/www-data/%s" % (project_name)
    current_base_dir = "%s/current" % (project_base_dir)
    service_base_dir = "%s/service" % (current_base_dir)
    with cd(current_base_dir):
        with prefix("source virtualenv/bin/activate"):
            upload_template(filename="utilities/build_settings.py", destination=service_base_dir)
            sudo("python service/manage.py collectstatic --noinput", user="www-data")

def create_tar_file(server, project_name, tarfile_name):
    project_base_dir = "/home/www-data/%s" % (project_name)
    current_dir = "%s/current" % (project_base_dir)
    with cd(current_dir):
        sudo("tar cfa %s service static virtualenv" % (tarfile_name), user='www-data')
        path_to_tarfile = '%s/%s' % (current_dir, tarfile_name)
        return path_to_tarfile

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
    ]
    def configure(self, server):
        git_url, svn_url = buildbot.splitter(self.parameter)

        # get project name from svn_url
        project_name = svn_checkout.root_folder(svn_url)

        # checkout deploy code to use in host machine
        # for using role
        checkout_deploy_sourcecode(server, project_name, git_url)
#        checkout_deploy_sourcecode_on_local(server, project_name, git_url)

        # create virtual environment from requirements.txt
        create_virtenv(server, project_name)

        # do collectstatic
        collect_static(server, project_name)

        # just get only build package name
        bpkg_name = get_build_package_name(server, svn_url)

        # create tar file
        path_to_tarfile = create_tar_file(server, project_name, bpkg_name)
        _logger.info("%s was created", path_to_tarfile)









