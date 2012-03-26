from fabric.context_managers import cd
from fabric.operations import run, sudo
from fabric.contrib.files import sed, exists
from fabric.context_managers import prefix
from profab.role import Role

def virtual_env_path(project_name):
    return "/home/www-data/Buildbot/%s/virtenv" % (project_name)

class Configure(Role):
    """
    Create Buildbot with parameter "project_name,git_url"
    """
    packages = [
        'build-essential',
        'python-dev',
        'python-setuptools',
        'git-core',
    ]
    def configure(self, server):
        server.cnx.create_tags([server.instance.id], {'buildbot':''})
        project_name, git_url = self.parameter.split(',')
        sudo('easy_install pip')
        sudo('easy_install virtualenv')
        virtenv_path = "/home/www-data/Buildbot/%s/virtenv" % (project_name)
        sudo("virtualenv --no-site-packages %s" % (virtenv_path), user="www-data")
        with prefix("source %s/bin/activate" % (virtenv_path)):
            sudo("pip install buildbot==0.8.4", user="www-data")
            sudo("pip install buildbot-slave", user="www-data")
            # Create buildbot-master and buildslave1.
            with cd("/home/www-data/Buildbot/%s" % (project_name)):
                sudo("buildbot create-master buildbot-master", user="www-data")
                sudo("buildslave create-slave buildslave1 localhost slave1 slave1password",user="www-data")
            # Assume that we already have buildslave1/builder-sqlite for checkout code.
            sudo("mkdir -p /home/www-data/Buildbot/%s/buildslave1/builder-sqlite" % (project_name), user="www-data")
            with cd("/home/www-data/Buildbot/%s/buildslave1/builder-sqlite" % (project_name)):
                sudo("git clone -q %s" % (git_url), user="www-data")
                # Point to develop branch
                git_folder = git_url.split('/')[-1]
                git_folder = git_folder.split('.')[0]
                with cd(git_folder):                   
                    sudo("git checkout -b develop", user="www-data")
                    sudo("git pull origin develop", user="www-data")
                    sudo("git checkout develop", user="www-data")
            sudo('cp' 
                 ' /home/www-data/Buildbot/%s/buildslave1/builder-sqlite/%s/buildbot/master.cfg' 
                 ' /home/www-data/Buildbot/%s/buildbot-master' % (project_name, git_folder, project_name), 
                user="www-data"
            )
        # Doing modify master.cfg.
        #with prefix("/home/www-data/Buildbot/%s/buildbot-master" % (project_name)):
        master_config_path = '/home/www-data/Buildbot/%s/buildbot-master' % (project_name)
        sed(master_config_path+"/master.cfg","/path/to/repo",git_url, use_sudo=True)
        sed(master_config_path+"/master.cfg","project_dirname",git_folder, use_sudo=True)
        with prefix("source %s/bin/activate" % (virtenv_path)):
            # Checking master.cfg.
            result = run("buildbot checkconfig %s/master.cfg" % (master_config_path))
            if "Config file is good" not in result:
                print "Something wrong with master.cfg, Buildbot won't start properly."
            with cd("/home/www-data/Buildbot/%s" % (project_name)):
                sudo("buildbot start buildbot-master", user="www-data")
                sudo("buildslave start buildslave1", user="www-data")

        server.cnx.create_tags([server.instance.id], {'buildbot':'installed'})

