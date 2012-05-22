from fabric.context_managers import cd
from fabric.operations import run, sudo
from fabric.contrib.files import sed, exists
from fabric.context_managers import prefix
from profab.role import Role

def virtual_env_path(root):
    return "%s/virtenv" % (root)

def home(project_name):
    return '/home/www-data/Buildbot/%s' % (project_name)

def project_base_folder(project_name):
    return '/home/www-data/%s' % (project_name)

def splitter(parameters):
    return parameters.split(',')

def split_private_git_url(git_url):
    user, remains = git_url.rsplit('@')
    host, path = remains.rsplit(':')
    return (user, host, path)

def master_virtual_env_path(root):
    virtenv_path = virtual_env_path(root)
    return '%s-master' % virtenv_path

def master_location(root):
    return '%s/buildbot-master' % (root)

def split_svn_url(svn_url):
    host = svn_url.split('.com')[0]+'.com'
    return host

def create_build_slave_layout(server, project_name):
    base_folder = '/home/www-data'
    with cd(base_folder):
        current_folder = '%s/current' % (project_name)
        config_folder = '%s/config' % (project_name)
        logs_folder = '%s/logs' % (project_name)
        bin_folder = '%s/bin' % (project_name)

        sudo('mkdir -p %s' % (current_folder), user="www-data") 
        sudo('mkdir -p %s' % (config_folder), user="www-data")
        sudo('mkdir -p %s' % (logs_folder), user="www-data")
        sudo('mkdir -p %s' % (bin_folder), user="www-data")

        sudo('mkdir -p %s/service' % (current_folder), user="www-data")
        sudo('mkdir -p %s/virtualenv' % (current_folder), user="www-data")
        sudo('mkdir -p %s/static' % (current_folder), user="www-data")

        buildbot_folder = '%s/buildbot' % (project_name)
        sudo('mkdir -p %s' % (buildbot_folder), user="www-data")
        sudo('mkdir -p %s/master' % (buildbot_folder), user="www-data")
        sudo('mkdir -p %s/slave1' % (buildbot_folder), user="www-data")


