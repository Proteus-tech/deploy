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
    

def create_build_slave_layout(server, project_name):
    base_folder = '/home/www-data'
    with cd(base_folder):
        current_folder = '%s/current' % (project_name)
        config_folder = '%s/config' % (project_name)
        logs_folder = '%s/logs' % (project_name)
        bin_folder = '%s/bin' % (project_name)

        sudo('mkdir -p %s' % (current_folder),user="www-data") 
        sudo('mkdir -p %s' % (config_folder),user="www-data")
        sudo('mkdir -p %s' % (logs_folder),user="www-data")
        sudo('mkdir -p %s' % (bin_folder),user="www-data")

        sudo('mkdir -p %s/service' % (current_folder),user="www-data")
        sudo('mkdir -p %s/virtualenv' % (current_folder),user="www-data")
        sudo('mkdir -p %s/static' % (current_folder),user="www-data")

        buildbot_folder = '%s/buildbot' % (project_name)
        sudo('mkdir -p %s' % (buildbot_folder),user="www-data")
        sudo('mkdir -p %s/master' % (buildbot_folder),user="www-data")
        sudo('mkdir -p %s/slave1' % (buildbot_folder),user="www-data")
        
        

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

