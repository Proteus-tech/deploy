from fabric.operations import sudo
from profab.role import Role
from proteus import buildbot

def create_symlink(server, from_path, to_path):
    sudo("ln -s %s %s" % (from_path, to_path), user="www-data")

class Configure(Role):
    """
    Create A symbolic link with parameter "from,to"
    """

    def configure(self, server):
        from_path, to_path = buildbot.splitter(self.parameter)
        create_symlink(server, from_path, to_path)

