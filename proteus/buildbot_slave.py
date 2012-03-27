from fabric.context_managers import cd
from fabric.operations import run, sudo
from fabric.contrib.files import sed, exists
from fabric.context_managers import prefix
from profab.role import Role

class Configure(Role):
    """
    Add buildbot slave for postgres 
    """
    def configure(self, server):
        server_tag = 'buildbot-slave-postgres'
        server.cnx.create_tags([server.instance.id], {server_tag:''})
        project_name = self.parameter
        limit_slave_number = 10
        # Check if pip and virtualenv are valid.
        if exists('/usr/local/bin/pip') and exists('/usr/local/bin/virtualenv'):
            virtenv_path = "/home/www-data/Buildbot/%s/virtenv-bb-slave" % (project_name)
            # Create virtual environment for buildbot slave
            sudo("virtualenv --no-site-packages %s" % (virtenv_path), user="www-data")
        with prefix("source %s/bin/activate" % (virtenv_path)):
            # Check if there has previous buildslave number
            # yes - increase buildslave number
            # no - create buildslave with current number
            with cd("/home/www-data/Buildbot/%s" % (project_name)):
                for number in range(1, limit_slave_number):
                    if exists('/home/www-data/Buildbot/%s/buildslave%d' % (project_name, number)):
                        continue
                    else:
                        sudo("buildslave create-slave buildslave%d localhost slave%d slave%dpassword" % 
                                (number, number, number) ,user="www-data")
                        break

                sudo("mkdir -p /home/www-data/Buildbot/%s/buildslave%d/builder-sqlite" % (project_name, number), user="www-data")
                with cd("/home/www-data/Buildbot/%s/buildslave%d/builder-sqlite" % (project_name, number)):
                    sudo("git clone -q %s" % (git_url), user="www-data")
                    # Point to develop branch
                    git_folder = git_url.split('/')[-1]
                    git_folder = git_folder.split('.')[0]
                    with cd(git_folder):                   
                        sudo("git checkout -b develop", user="www-data")
                        sudo("git pull origin develop", user="www-data")
                        sudo("git checkout develop", user="www-data")

        with prefix("source %s/bin/activate" % (virtenv_path)):
            # Checking master.cfg.
            result = run("buildbot checkconfig %s/master.cfg" % (master_config_path))
            if "Config file is good" not in result:
                print "Something wrong with master.cfg, Buildbot won't start properly."
            with cd("/home/www-data/Buildbot/%s" % (project_name)):
                sudo("buildbot restart buildbot-master", user="www-data")
                sudo("buildslave start buildslave1", user="www-data")

        server.cnx.create_tags([server.instance.id], {server_tag:'installed'})

