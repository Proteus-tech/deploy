#!/usr/bin/env python

from fabric.context_managers import prefix, cd
from fabric.operations import run, sudo
from proteus import buildbot as buildbot_utils
from profab.role import Role

version = 'develop'
proteus_deploy_git_url = 'git@github.com:Proteus-tech/deploy.git@%s' % (version)

def create_virtenv_base_project(server, project_name, virtenv_name):
    project_base_folder = buildbot_utils.home(project_name)
    command_list = ['virtualenv','--no-site-packages',virtenv_name]
    with cd(project_base_folder):
        sudo(' '.join(command_list), user="www-data")
        virtualenv_base_folder = '%s/%s' % (project_base_folder, virtenv_name)
        with prefix("source %s/bin/activate" % (virtenv_name)):
            sudo("pip install buildbot-slave==0.8.5")
            sudo("pip install {0}".format(proteus_deploy_git_url),user="www-data")



class Configure(Role):
    """
        install_buildbot_environment "<project-name>,<virtenv-name>"
    """
    def configure(self,server):
        project_name, virtenv_name = buildbot_utils.splitter(self.parameter)
        create_virtenv_base_project(server, project_name, virtenv_name)



