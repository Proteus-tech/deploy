from ast import literal_eval
from fabric.context_managers import cd
from fabric.contrib.files import exists, sed
from fabric.operations import sudo
from profab.role import Role

def create_user(server, dict_data):
    user = dict_data['USER']
    password = dict_data['PASSWORD']
    sudo('''psql -c "CREATE USER %s WITH PASSWORD '%s';" -U postgres''' 
         % (user, password))

def create_db(server, dict_data):
    name = dict_data['NAME']
    user = dict_data['USER']
    sudo('createdb %s -O %s -U postgres' % (name, user))

def setup(server, project_name):
    project_path = '/home/www-data/Buildbot/%s' % project_name

    if exists(project_path):
        src_path = '%s/buildslave1/builder-pg/src' % project_path
        with cd(src_path):
            dict_data = sudo('python -c "project = \'%s_project\''
                 ';pg_buildbot = '
                 '__import__(\'%s_project.settings.pg_buildbot\'' 
                 ', fromlist=[project, \'settings\'])' 
                 ';print pg_buildbot.DATABASES[\'default\']"' 
                 % (project_name, project_name)
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
        project_name = self.parameter
        dict_data = setup(server, project_name)
        create_user(server,dict_data)
        create_db(server,dict_data)
