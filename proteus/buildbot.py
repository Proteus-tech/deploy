from fabric.context_managers import cd
from fabric.operations import run, sudo
from fabric.contrib.files import sed, exists
from fabric.context_managers import prefix
from profab.role import Role

def virtual_env_path(root):
    return "%s/virtenv" % (root)

def home(project_name):
    return '/home/www-data/Buildbot/%s' % (project_name)

def splitter(parameters):
    return parameters.split(',')

def split_private_git_url(git_url):
    user, remains = git_url.rsplit('@')
    host, path = remains.rsplit(':')
    return (user, host, path)


