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
    master_checkout_parameters = '%s,%s' % (root, repository)
    master_path = '%s/buildbot-master' % (root) 
    master_cfg_src = '%s/src/buildbot/master.cfg' % (root)
    master_cfg_dest = '%s/master.cfg' % (master_path)
    complete_params = '%s,%s' % (master_cfg_dest, repository)
    # slave parameters
    slave_path = '%s/buildslave1' % (root)
    slave_checkout_path = "%s/builder-sqlite" % (slave_path)
    slave_checkout_parameters = '%s,%s' % (slave_checkout_path, repository)
    slave_setup_params = '%s,%s,%s' % (root,'slave1','localhost')
    role_tuple_list += [
         ('proteus.install_buildbot_master_env', master_virtenv)
        ,('proteus.tag', 'master,env-installed')
        ,('proteus.setup_buildbot_master', root)
        ,('proteus.git_checkout', master_checkout_parameters)
        ,('proteus.create_symlink', '%s,%s' % (master_cfg_src, master_cfg_dest))
        ,('proteus.complete_master_config', complete_params)
        ,('proteus.check_config','%s,%s' % (master_cfg_dest, master_virtenv))
        ,('proteus.tag', 'master,ready')
        ,('proteus.install_buildbot_slave_env', slave_virtenv)
        ,('proteus.tag', 'slave,env-installed')
        ,('proteus.setup_buildbot_slave', slave_setup_params)
        ,('proteus.git_checkout', slave_checkout_parameters)
        ,('proteus.tag', 'slave,ready')
        ,('proteus.start_buildbot_master', '%s,%s' % (master_path, master_virtenv))
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
    slave_checkout_path = "%s/builder-sqlite" % (slave_path)
    slave_checkout_parameters = '%s,%s' % (slave_checkout_path, repository)
    slave_setup_params = '%s,%s,%s' % (root,'slave1', ec2_master_host)

    role_tuple_list += [
        ('proteus.install_buildbot_slave_env', slave_virtenv)
        ,('proteus.tag', 'slave,env-installed')
        ,('proteus.setup_buildbot_slave', slave_setup_params)
        ,('proteus.git_checkout', slave_checkout_parameters)
        ,('proteus.tag', 'slave,ready')
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

