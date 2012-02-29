from profab.server import Server
import simpleserver

def add_buildbot(server, project_name, git_url):
    role_tuple_list = [
        ('proteus.buildbot','%s,%s' % (project_name, git_url) ),
    ]
    server.add_roles( server.get_role_adders(*role_tuple_list) )

def setup( using_client, dest_url, project_name, git_url ):
    '''
    Adding buildbot role : using_client, dest_url, project_name, git_url
    '''
    server = Server.connect( client=using_client, hostname=dest_url )
    if server:
        add_buildbot(server, project_name, git_url)
    
def start( using_client, project_name, repository, *args):
    server = simpleserver.start(using_client, *args)
    add_buildbot(server, project_name, repository)

