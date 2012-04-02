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

    root = "/home/www-data/Buildbot/%s" % (project_name)
    # virtual environment
    virtenv_path = virtual_env_path(root)
    master_virtenv = '%s-master' % virtenv_path
    slave_virtenv = '%s-slave' % virtenv_path
    # master parameters
    master_path = '%s/buildbot-master' % (root) 
    # slave parameters
    slave_path = '%s/buildslave1' % (root)
    role_tuple_list += [
         ('proteus.buildbot_master', repository)
        ,('proteus.buildbot_slave', repository)
        ,('proteus.start_buildbot_master', project_name)
        ,('proteus.start_buildbot_slave', '%s,%s' % (slave_path, slave_virtenv))
        ,('smarthost',None)
        ,('proteus.tag', 'mta,exim4')
        ,('proteus.tag', 'buildbot,combo-%s' % project_name)
        ,('proteus.tag', 'Name,buildbot-%s' % project_name)
    ]
    server.add_roles( server.get_role_adders(*role_tuple_list) )

def add_buildbot_slave(server, project_name, ec2_master_host, repository, privacy):
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
    root = "/home/www-data/Buildbot/%s" % (project_name)
    # virtual environment
    virtenv_path = virtual_env_path(root)
    slave_virtenv = '%s-slave' % virtenv_path
    # slave parameters
    slave_path = '%s/buildslave1' % (root)
    slave_params = '%s,%s' % (repository, ec2_master_host)

    role_tuple_list += [
        ('proteus.buildbot_slave', slave_params)
    ]  
    server.add_roles( server.get_role_adders(*role_tuple_list) )

def setup_buildbot_slave(using_client, ec2_host, ec2_master_host, project_name, repository, privacy='public'):
    '''
    Adding buildbot slave role : using_client, ec2_host, ec2_master_host, project_name, repository
    '''
    server = Server.connect( client=using_client, hostname=ec2_host )
    if server:
        add_buildbot_slave( server, project_name, ec2_master_host, repository, privacy )

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

def restart_buildbot_master(using_client, ec2host, project_name):
    root = "/home/www-data/Buildbot/%s" % (project_name)
    buildbot_master_path = '%s/buildbot-master' % (root)
    buildbot_virtenv = virtual_env_path(root)
    buildbot_master_virtenv = '%s-master' % (buildbot_virtenv)
    server = Server.connect( client=using_client, hostname=ec2host )
    role_tuple_list = [
         ('proteus.restart_buildbot_master','%s,%s' % (buildbot_master_path, buildbot_master_virtenv))
    ]
    server.add_roles( server.get_role_adders(*role_tuple_list) )

def restart_buildbot_slave(using_client, ec2host, project_name):
    root = "/home/www-data/Buildbot/%s" % (project_name)
    buildbot_slave_path = '%s/buildslave1' % (root)
    buildbot_virtenv = virtual_env_path(root)
    buildbot_slave_virtenv = '%s-slave' % (buildbot_virtenv)
    server = Server.connect( client=using_client, hostname=ec2host )
    role_tuple_list = [
         ('proteus.restart_buildbot_slave','%s,%s' % (buildbot_slave_path, buildbot_slave_virtenv))
    ]
    server.add_roles( server.get_role_adders(*role_tuple_list) )

