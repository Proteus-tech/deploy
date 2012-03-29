from profab.role import Role
from proteus.git_checkout import root_folder, git_checkout

class Configure(Role):
    """
    Add buildbot Slave with parameter "repository" 
    """
    packages = [ 'build-essential'
        , 'python-dev'
        , 'python-setuptools'
        , 'git-core'
    ]

    def configure(self, server):
        repository = self.parameter 
        project_name = root_folder(repository)

