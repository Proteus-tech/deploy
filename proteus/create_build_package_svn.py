#!/usr/bin/env python


from fabric.context_managers import cd
from fabric.api import sudo

from proteus import buildbot as buildbot_utils
from proteus import buildbot_build_utils as build_utils
from proteus import svn_checkout

from profab.role import Role
from profab import _logger

def _get_project_name(svn_url):
    project_name = None
    if svn_url.endswith('/'):
        project_name = svn_url.rstrip('/').split('/')[-2]
    else:
        project_name = svn_url.split('/')[-2]
    return project_name

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
        ubuntu_version, bits = build_utils.get_machine_spec(server)

        return "%s.%s.%s.%s.tar" % (project_name, svn_rev, ubuntu_version, bits)

def remove_svn_hidden_folder(server, project_name):
    code_path = '/home/www-data/%s/current/service' % (project_name)
    with cd(code_path):
        sudo("find -name '.svn' | xargs rm -rf", user="www-data")

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
        git_url, svn_url = buildbot_utils.splitter(self.parameter)

        # get project name from svn_url
        project_name = svn_checkout.root_folder(svn_url)

        # checkout deploy code to use in host machine
        # for using role
        build_utils.checkout_deploy_sourcecode(server, project_name, git_url)

        # clean svn hidden folder of project dir
        remove_svn_hidden_folder(server, project_name)

        # create virtual environment from requirements.txt
        build_utils.create_virtenv(server, project_name)

        # do collectstatic
        build_utils.collect_static(server, project_name)

        # just get only build package name
        bpkg_name = get_build_package_name(server, svn_url)

        # create tar file
        path_to_tarfile = build_utils.create_tar_file(server, project_name, bpkg_name)
        _logger.info("%s was created", path_to_tarfile)









