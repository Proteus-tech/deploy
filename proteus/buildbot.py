from fabric.context_managers import cd
from fabric.operations import run, sudo
from fabric.contrib.files import sed
from profab.role import Role

class AddRole(Role):
    """
    Create Buildbot with parameter "project_name,git_url"
    """
    packages = ['python-setuptools','git-core','git-flow']
    def configure(self, server):
        project_name, git_url = self.parameter.split(',')
        sudo('easy_install pip')
        sudo('easy_install virtualenv')
        virtenv_path = "/home/www-data/Buildbot/%s/virtenv" % (project_name)
        sudo("virtualenv %s" % (virtenv_path), user="www-data")
        with prefix("source %s/bin/activate" % (virtenv_path)):
            sudo("pip install buildbot", user="www-data")
            sudo("pip install buildbot-slave", user="www-data")
            # Create buildbot-master and buildslave1.
            with cd("/home/www-data/Buildbot/%s" % (project_name)):
                sudo("buildbot create-master buildbot-master", user="www-data")
                sudo("buildslave create-slave buildslave1 localhost slave1 slave1password" user="www-data")
            # Assume that we already have buildslave1/builder-sqlite for checkout code.
            with cd("/home/www-data/Buildbot/%s/buildslave1/builder-sqlite" % (project_name)):
                sudo("git clone %s" % (git_url), user="www-data")
                git_folder = git_url.split('/')[-1]
                with cd("%s" % (git_folder)):
                    sudo("pip install --requirement=setup/requirements.txt", user="www-data")
                    # Use -d to bypass whenever prompt come up.
                    sudo("git flow init -d", user="www-data")
            sudo('cp <somewhere master.cfg> /home/www-data/Buildbot/%s/buildbot-master', user="www-data")
            # Doing modify master.cfg.
            with cd("/home/www-data/Buildbot/%s/buildbot-master" % (project_name)):
                sed("master.cfg","/path/to/repo",gir_url)
                sed("master.cfg","project",project_name)
                # Checking master.cfg.
                result = run("buildbot checkconfig master.cfg")
                if "Config file is good" not in result:
                    print "Something wrong with master.cfg, Buildbot won't start."
            with cd("/home/www-data/Buildbot/%s" % (project_name)):
                sudo("buildbot start buildbot-master", user="www-data")
                sudo("buildslave start buildslave1", user="www-data")

