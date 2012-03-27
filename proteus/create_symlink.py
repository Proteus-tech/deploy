from fabric.operations import sudo
from profab.role import Role
from proteus import buildbot

class Configure(Role):
    """
    Create A symbolic link with parameter "from,to"
    """

    def configure(self, server):
        from_path, to_path = buildbot.splitter(self.parameter)
        sudo("ln -s %s %s" % (from_path, to_path), user="www-data")

