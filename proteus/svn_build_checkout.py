from fabric.context_managers import cd
from fabric.operations import sudo, run
from fabric.contrib.files import append, exists
from profab.role import Role
from proteus import buildbot
from proteus import svn_checkout

def svn_build_checkout(server, svn_url, path):
    with cd(path):
        svn_folder = 'current/service'
        sudo("svn co --username 'www-data' \
                     --password 'www-d@t@!@#' \
                     --force \
                     --trust-server-cert \
                     --non-interactive %s %s" % (svn_url, svn_folder)
                ,user="www-data")

        with cd(svn_folder):
            sudo("svn update --username 'www-data' \
                             --password 'www-d@t@!@#' \
                             --force \
                             --trust-server-cert \
                             --non-interactive"
                ,user="www-data")
    

class Configure(Role):
    """
    Checkout code from svn repository with path ( on build server )
    Description
    - path : should be project folder 
             ex. 
    - svn_url
    """
    packages = ['subversion']

    def configure(self, server):
        svn_url = self.parameter
        project_name = svn_checkout.root_folder(svn_url)
        project_base_folder = buildbot.project_base_folder(project_name) 
        buildbot.create_build_slave_layout(server, project_name)
        svn_build_checkout(server, svn_url, project_base_folder)

