from profab.server import Server
from proteus.buildbot import virtual_env_path 
import simpleserver

def split_private_git_url(git_url):
    user, remains = git_url.rsplit('@')
    host, path = remains.rsplit(':')
    return (user, host, path)

def add_buildbot(server, project_name, repository, privacy):
    role_tuple_list = [
        ('proteus.www_home',''),
    ]
    if privacy == 'private':
        print 'do hand shaking for private repository'
        user, host, path = split_private_git_url(repository)
        role_tuple_list += [
            ('proteus.ssh_key_gen', ''),
            ('proteus.authorize_key', repository),
            ('proteus.trust_host', host),
        ]
    virtenv_path = virtual_env_path(project_name)
    buildbot_master_virtenv = '%s-master' % virtenv_path
    buildbot_slave_virtenv = '%s-slave' % virtenv_path
    master_checkout_path = "/home/www-data/Buildbot/%s" % (project_name)
    master_checkout_parameters = '%s,%s' % (master_checkout_path, repository)
    buildbot_slave_path = '/home/www-data/Buildbot/%s/buildslave1' % (project_name)
    slave_checkout_path = "%s/builder-sqlite" % (buildbot_slave_path)
    buildbot_master_path = '/home/www-data/Buildbot/%s/buildbot-master' % (project_name) 
    master_cfg_src = '/home/www-data/Buildbot/%s/src/buildbot/master.cfg' % (project_name)
    master_cfg_dest = '%s/master.cfg' % (buildbot_master_path)
    complete_params = '%s,%s' % (master_cfg_dest, repository)
    slave_params = '%s,%s,%s' % (project_name,'slave1','localhost')
    role_tuple_list += [
        ('proteus.install_buildbot_master_env', buildbot_master_virtenv)
        ,('proteus.setup_buildbot_master', project_name)
        ,('proteus.git_checkout', master_checkout_parameters)
        ,('proteus.create_symlink', '%s,%s' % (master_cfg_src, master_cfg_dest))
        ,('proteus.complete_master_config', complete_params)
        ,('proteus.check_config','%s,%s' % (master_cfg_dest, buildbot_master_virtenv))
        ,('proteus.install_buildbot_slave_env', buildbot_slave_virtenv)
        ,('proteus.setup_buildbot_slave', slave_params)
        ,('proteus.start_buildbot_master', '%s,%s' % (buildbot_master_path, buildbot_master_virtenv))
        ,('proteus.start_buildbot_slave', '%s,%s' % (buildbot_slave_path, buildbot_slave_virtenv))
        ,('proteus.buildbot','%s,%s' % (project_name, repository) )
        ,('smarthost',None)
    ]
    server.add_roles( server.get_role_adders(*role_tuple_list) )

def setup(using_client, ec2_host, project_name, repository, privacy='public'):
    '''
    Adding buildbot role : using_client, ec2_host, project_name, repository
    '''
    server = Server.connect( client=using_client, hostname=ec2_host )
    if server:
        add_buildbot(server, project_name, repository, privacy)
    
def start(using_client, project_name, repository, privacy='public', *args):
    server = simpleserver.start(using_client, *args)
    add_buildbot(server, project_name, repository, privacy)

