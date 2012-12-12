from ast import literal_eval
from fabric.context_managers import cd
from fabric.contrib.files import exists, sed
from fabric.operations import sudo
from profab.role import Role
from proteus import buildbot, git_checkout

def create_user(server, dict_data):
    user = dict_data['USER']
    password = dict_data['PASSWORD']
    sudo('''psql -c "CREATE USER %s WITH PASSWORD '%s' CREATEDB;" -U postgres''' 
         % (user, password))

def create_db(server, dict_data):
    name = dict_data['NAME']
    user = dict_data['USER']
    sudo('createdb %s -O %s -U postgres' % (name, user))

def setup(server, param):
    project_name, repository = buildbot.splitter(param)
    project_path = '/home/www-data/Buildbot/%s' % project_name
    root_folder_name = git_checkout.root_folder(repository)
    if exists(project_path):
        src_path = '%s/buildslave2/builder-pg/src' % project_path
        with cd(src_path):
            dict_data = sudo('python -c "project = \'%s_project\''
                 ';pg_buildbot = '
                 '__import__(\'%s_project.settings.pg_buildbot\'' 
                 ', fromlist=[project, \'settings\'])' 
                 ';print pg_buildbot.DATABASES[\'default\']"' 
                 % (root_folder_name, root_folder_name)
                ,user = 'www-data')
    else:
        msg = '[Error] Don\'t have %s project.' % project_name
        raise Exception(msg)
    
    tmp_dict = literal_eval(dict_data)
    return tmp_dict


class Configure(Role):
    '''
    Create postgres database and user.
    '''
    def configure(self, server):
        dict_data = setup(server, self.parameter)
        create_user(server,dict_data)
        create_db(server,dict_data)

