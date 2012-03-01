from profab.server import Server
import simpleserver

def add_buildbot(server, project_name, repository):
    role_tuple_list = [
        ('proteus.buildbot','%s,%s' % (project_name, repository) ),
    ]
    server.add_roles( server.get_role_adders(*role_tuple_list) )

def setup( using_client, ec2_host, project_name, repository ):
    '''
    Adding buildbot role : using_client, ec2_host, project_name, repository
    '''
    server = Server.connect( client=using_client, hostname=ec2_host )
    if server:
        add_buildbot(server, project_name, repository)
    
def start( using_client, project_name, repository, *args):
    server = simpleserver.start(using_client, *args)
    add_buildbot(server, project_name, repository)

