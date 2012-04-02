from fabric.context_managers import cd
from fabric.operations import sudo
from fabric.contrib.files import append
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
        , "cd /home/www-data/Buildbot/$1/src"
        , "git pull origin develop"
    ]
    binary_folder = '%s/bin' % (path)
    with cd(binary_folder):
        sudo('touch update_master_config', user='www-data')
        sudo('chmod 755 update_master_config', user='www-data')
        append(filename='update_master_config', text=script_content, use_sudo=True)

class Configure(Role):
    """
    Checkout code from git_url to a path with parameters (git_url, path)
    """
    packages = ['git-core']

    def configure(self, server):
        path, git_url = buildbot.splitter(self.parameter)
        git_checkout(server, path, git_url)
        create_script_to_update_master_config(server, path)

