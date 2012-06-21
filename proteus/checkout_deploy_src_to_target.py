#!/usr/bin/env python

from fabric.context_managers import cd
from fabric.operations import sudo
from fabric.contrib.files import exists
from profab.role import Role

def checkout_deploy_src_to_target(server, project_name, git_url=None, target_path=None, branch='develop'):
    buildbot_project_base_folder = '/home/www-data/Buildbot/%s'
    if git_url is None:
        git_url = 'git://github.com/Proteus-tech/deploy.git'
    if target_path is None:
        target_path = buildbot_project_base_folder % (project_name)

    with cd(target_path):
        deploy_src_path = '%s/deploy' % (target_path)
        if not exists(deploy_src_path):
            sudo("git clone -q %s %s" % (git_url, deploy_src_path), user="www-data")
            # Point to develop branch
            with cd(deploy_src_path):
                sudo("git checkout -b %s" % (branch), user="www-data")
                sudo("git pull origin %s" % (branch), user="www-data")
                sudo("git checkout %s" % (branch), user="www-data")


class Configure(Role):
    """
    Checkout specific deploy code to target destination
    """
    packages = ['git-core']

    def configure(self, server):
        project_name = self.parameter
        checkout_deploy_src_to_target(server, project_name)


