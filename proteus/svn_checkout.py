from fabric.context_managers import cd
from fabric.operations import sudo
from fabric.contrib.files import append, exists
from profab.role import Role
from proteus import buildbot

def root_folder(svn_url):
    return svn_url.split('/')[-1]

def svn_checkout(server, path, svn_url):
    with cd(path):
        svn_folder = 'src'
        sudo("svn co --username 'www-data' --password 'www-d@t@!@#' --force --trust-server-cert --non-interactive %s/trunk %s" % (svn_url, svn_folder), user="www-data")
        # Point to develop branch
        with cd(svn_folder):
            sudo("svn update --username 'www-data' --password 'www-d@t@!@#' --force --trust-server-cert --non-interactive", user="www-data")

def create_script_to_update_master_config(server, path):
    # Update latest code
    script_content = ["#!/bin/bash"
        , "if [ $# -eq 1 ]; then"
        , "cd /home/www-data/Buildbot/$1/src"
        , "svn update --username 'www-data' --password 'www-d@t@!@#' --force --trust-server-cert --non-interactive"
        , "fi"
    ]
    binary_folder = '%s/bin' % (path)
    script_file = '%s/update_master_config' % (binary_folder)
    sudo('mkdir -p %s' % (binary_folder), user='www-data')
    with cd(binary_folder):
        if not exists(script_file):
            sudo('touch update_master_config', user='www-data')
            sudo('chmod 755 update_master_config', user='www-data')
            append(filename='update_master_config', text=script_content, use_sudo=True)

class Configure(Role):
    """
    Checkout code from svn_url to a path with parameters (path, svn_url)
    """
    packages = ['subversion']

    def configure(self, server):
        path, svn_url = buildbot.splitter(self.parameter)
        svn_checkout(server, path, svn_url)
        create_script_to_update_master_config(server, path)

