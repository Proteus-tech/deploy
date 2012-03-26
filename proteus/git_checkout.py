from profab.role import Role

def root_folder(git_url):
    git_folder = git_url.split('/')[-1]
    return git_folder.split('.git')[0]

class Configure(Role):
    """
    Checkout code from git_url to a path with parameters (git_url, path)
    """
    def configure(self, server):
        path = "/home/www-data/Buildbot/%s/buildslave1/builder-sqlite" % (project_name)
        git_url = ''
        with cd(path):
            sudo("git clone -q %s" % (git_url), user="www-data")
            # Point to develop branch
            git_folder = root_folder(git_url)
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
 
