from fabric.context_managers import cd
from fabric.operations import sudo
from fabric.contrib.files import append, exists
from profab.role import Role
from proteus import buildbot

def svn_build_checkout(server, path, svn_url):
    with cd(path):
        svn_folder = 'current'
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

        run('mkdir -p %s' % (current_folder)) 
        run('mkdir -p %s' % (config_folder))
        run('mkdir -p %s' % (logs_folder))
        run('mkdir -p %s' % (bin_folder))

        run('mkdir -p %s/service' % (current_folder))
        run('mkdir -p %s/virtualenv' % (current_folder))
        run('mkdir -p %s/static' % (current_folder))

        buildbot_folder = '%s/buildbot' % (project_name)
        run('mkdir -p %s' % (buildbot_folder))
        run('mkdir -p %s/master' % (buildbot_folder))
        run('mkdir -p %s/slave1' % (buildbot_folder))
        
        

class Configure(Role):
    """
    Checkout code from svn repository with path ( on build server )
    Description
    - path : should be project folder 
             ex. 
    """
    packages = ['subversion']

    def configure(self, server):
        path, svn_url = buildbot.spitter(self.parameter)
        create_build_slave_layout(server, project_name)
        svn_build_checkout(server)

