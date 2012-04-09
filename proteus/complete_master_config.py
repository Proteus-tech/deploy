from fabric.contrib.files import sed
from profab.role import Role
from buildbot import splitter

def complete_master_config(server, config_file, git_url):
    sed(config_file,'/path/to/repo', git_url, use_sudo=True)
    sed(config_file,'project_dirname', 'src', use_sudo=True)
    sed(config_file,'buildbot_master_host', server.instance.dns_name, use_sudo=True)

class Configure(Role):
    '''
    Complete Buildbot Master configuration file with "config_full_path,git_url"    
    '''
    def configure(self, server):
        config_file, git_url = splitter(self.parameter)
        complete_master_config(server, config_file, git_url)

