from fabric.context_managers import cd
from fabric.operations import sudo
from fabric.contrib.files import append, exists
from profab.role import Role
from proteus import buildbot

def root_folder(git_url):
    git_folder = git_url.split('/')[-1]
    return git_folder.split('.git')[0]

def git_checkout(server, path, git_url):
    with cd(path):
        git_folder = 'src'
        sudo("git clone -q %s %s" % (git_url, git_folder), user="www-data")
        # Point to develop branch
        with cd(git_folder):                   
            sudo("git checkout -b develop", user="www-data")
            sudo("git pull origin develop", user="www-data")
            sudo("git checkout develop", user="www-data")

def create_script_to_update_master_config(server, path):
    # Update latest code
    script_content = ["#!/bin/bash"
        , "if [ $# -eq 1 ]; then"
        , "cd /home/www-data/Buildbot/$1/src"
        , "git pull origin develop"
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
    Checkout code from git_url to a path with parameters (path, git_url)
    """
    packages = ['git-core']

    def configure(self, server):
        path, git_url = buildbot.splitter(self.parameter)
        git_checkout(server, path, git_url)
        create_script_to_update_master_config(server, path)

