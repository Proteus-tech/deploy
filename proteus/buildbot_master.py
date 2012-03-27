from profab.role import Role
from proteus.buildbot import virtual_env_path 
from proteus.create_symlink import create_symlink
from proteus.complete_master_config import complete_master_config 
from proteus.git_checkout import root_folder, git_checkout
from proteus.install_buildbot_master_env import install_buildbot_master_env
from proteus.setup_buildbot_master import setup_buildbot_master
from proteus.tag import tag

class Configure(Role):
    """
    Setup Buildbot Master with parameter "repository"
    """
    packages = [ 'build-essential'
        , 'python-dev'
        , 'python-setuptools'
    ]

    def configure(self, server):
        repository = self.parameter 
        project_name = root_folder(repository)
        root = "/home/www-data/Buildbot/%s" % (project_name)
 
        virtenv_path = virtual_env_path(root)
        master_virtenv = '%s-master' % virtenv_path
        install_buildbot_master_env(server, master_virtenv)
        tag(server, 'master', 'env-installed')

        setup_buildbot_master(server, root) 
        git_checkout(server, root, repository)

        master_path = '%s/buildbot-master' % (root) 
        master_cfg_src = '%s/src/buildbot/master.cfg' % (root)
        master_cfg_dest = '%s/master.cfg' % (master_path)
        create_symlink(server, master_cfg_src, master_cfg_dest)

        complete_master_config(server, master_cfg_dest, repository)

