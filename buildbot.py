from profab.server import Server
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
    role_tuple_list += [
        ('proteus.buildbot','%s,%s' % (project_name, repository) ),
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

