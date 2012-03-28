from fabric.context_managers import cd
from fabric.operations import run, sudo
from fabric.contrib.files import sed, exists
from fabric.context_managers import prefix
from profab.role import Role

def virtual_env_path(root):
    return "%s/virtenv" % (root)

def splitter(parameters):
    return parameters.split(',')

