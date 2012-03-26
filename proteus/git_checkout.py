class Configure(Role):
    def configure(self, server):
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
 
