#!/usr/bin/env python

from fabric.context_managers import cd
from fabric.api import sudo

from proteus import buildbot as buildbot_utils
from proteus import buildbot_build_utils as build_utils
from proteus import git_checkout

from profab.role import Role
from profab import _logger

def _get_project_name(url):
    git_url = url
    project_name = None
    if git_url[:3]=='git':
        if git_url.endswith('/'):
            project_name = git_url.rstrip('/').split('/')[-1].split('.')[0]
        else:
            project_name = git_url.split('/')[-1].split('.')[0]
    elif git_url[:3]=='ssh':
        if git_url.endswith('/'):
            project_name = git_url.rstrip('/').split('/')[-1]
        else:
            project_name = git_url.split('/')[-1]
    return project_name


def get_build_package_name(server, url):
    project_name = _get_project_name(url)
    service_dir = "/home/www-data/%s/current/service" % (project_name)
    with cd(service_dir):
        std_out = sudo("git log -n 1",user="www-data")
        sha = std_out.split('\n')[0].split(' ')[1]
        rev = sha[:40]
        ubuntu_version, bits = build_utils.get_machine_spec(server)
        return "%s.%s.%s.%s.tar" % (project_name, rev, ubuntu_version, bits)

def remove_git_hidden_folder(server, project_name):
    code_path = '/home/www-data/%s/current/service' % (project_name)
    with cd(code_path):
        sudo("rm -rf .git", user="www-data")
        sudo("rm -rf .gitignore", user="www-data")

class Configure(Role):
    """
    Create build package, then upload to s2
    - usage
        --proteus.create_build_package_svn git_url,svn_url
        * git_url : deploy git 
            should be "git://github.com/Proteus-tech/deploy.git" 
        ** git_url : project git
    """
    packages = [
        'python-setuptools',
        'git-core'
        ]
    def configure(self, server):
        git_url, project_url = buildbot_utils.splitter(self.parameter)

        # get project name from svn_url
        project_name = git_checkout.root_folder(project_url)

        # checkout deploy code to use in host machine
        # for using role
        build_utils.checkout_deploy_sourcecode(server, project_name, git_url)

        # create virtual environment from requirements.txt
        build_utils.create_virtenv(server, project_name)

        # do collectstatic
        build_utils.collect_static(server, project_name)

        # just get only build package name
        bpkg_name = get_build_package_name(server, project_url)

        # clean svn hidden folder of project dir
        remove_git_hidden_folder(server, project_name)

        # create tar file
        path_to_tarfile = build_utils.create_tar_file(server, project_name, bpkg_name)
        _logger.info("%s was created", path_to_tarfile)









