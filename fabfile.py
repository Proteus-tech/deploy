import buildbot, simpleserver
from profab.server import Server

def simple_server(using_client, *args):
    '''
    Create simple server : using_client, bits, region, ami
    '''
    return simpleserver.start(using_client, *args)

def create_buildbot( using_client, dest_url, project_name, git_url ):
    '''
    Adding buildbot role : using_client, dest_url, project_name, git_url
    '''
    buildbot.setup(using_client, dest_url, project_name, git_url)

