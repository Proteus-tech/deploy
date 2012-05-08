from profab.role import Role
from proteus.buildbot import master_virtual_env_path, home, master_location
from proteus.check_config import check_config
from proteus.create_symlink import create_symlink
#from proteus.git_checkout import root_folder, git_checkout, create_script_to_update_master_config 
from proteus.svn_checkout import svn_checkout

from proteus.install_buildbot_master_env import install_buildbot_master_env
from proteus.setup_buildbot_master import setup_buildbot_master
from proteus.tag import tag
from proteus import buildbot

class Configure(Role):
    """
    Setup Buildbot Master with parameter "repository"
    """
    packages = [ 'build-essential'
        , 'python-dev'
        , 'python-setuptools'
        , 'git-core'
    ]

    def configure(self, server):
        repository, project_name = buildbot.splitter(self.parameter) 
        root = home(project_name)
 
        master_virtenv = master_virtual_env_path(root)
        install_buildbot_master_env(server, master_virtenv)
        tag(server, 'master', 'env-installed')

        setup_buildbot_master(server, root) 
        git_checkout(server, root, repository)
        create_script_to_update_master_config(server, root)

        master_path = master_location(root) 
        master_src = '%s/src' % (root)
        master_cfg_src = '%s/buildbot_config/master_svn.cfg' % (master_src)
        master_cfg_settings = '%s/buildbot_config/settings.py' % (master_src)
        master_cfg_dest = '%s/master.cfg' % (master_path)
        create_symlink(server, master_cfg_src, master_cfg_dest)

        check_config(server, master_cfg_dest, master_virtenv, master_src)
        tag(server, 'master', 'ready')

