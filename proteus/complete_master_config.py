from fabric.contrib.files import sed
from profab.role import Role
from buildbot import splitter


class Configure(Role):
    '''
    Complete Buildbot Master configuration file with "master_config_full_path,git_url"    
    '''
    def configure(self, server):
        master_config_file, git_url = splitter(self.parameter)
        sed(master_config_file,'/path/to/repo', git_url, use_sudo=True)
        sed(master_config_file,'project_dirname', 'src', use_sudo=True)

