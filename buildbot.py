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
    master_checkout_path = "/home/www-data/Buildbot/%s" % (project_name)
    master_checkout_parameters = '%s,%s' % (master_checkout_path, repository)
    slave_checkout_path = "/home/www-data/Buildbot/%s/buildslave1/builder-sqlite" % (project_name)
    master_cfg_src = '/home/www-data/Buildbot/%s/src/buildbot/master.cfg' % (project_name)
    master_cfg_dest = '/home/www-data/Buildbot/%s/buildbot-master/master.cfg' % (project_name)
    complete_params = '%s,%s' % (master_cfg_dest, repository)
    role_tuple_list += [
        ('proteus.install_buildbot_master_env', '%s-master' % virtenv_path)
        ,('proteus.setup_buildbot_master', project_name)
        ,('proteus.git_checkout', master_checkout_parameters)
        ,('proteus.create_symlink', '%s,%s' % (master_cfg_src, master_cfg_dest))
        ,('proteus.complete_master_config', complete_params)
        ,('proteus.install_buildbot_slave_env', '%s-slave' % virtenv_path)
        ,('proteus.check_config','%s,%s' % (master_cfg_dest,'%s-master' % (virtenv_path)))
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

