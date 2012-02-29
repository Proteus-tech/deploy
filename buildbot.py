from profab.server import Server

def setup( using_client, dest_url, project_name, git_url ):
    '''
    Adding buildbot role : using_client, dest_url, project_name, git_url
    '''
    print 'using client = ', using_client
    print 'dest_url = ', dest_url
    print 'project_name = ', project_name
    print 'git_url', git_url 
    s = Server.connect( client=using_client, hostname=dest_url )
    if s:
        role_tuple_list = [
            ('proteus.buildbot','%s,%s' % (project_name, git_url) ),
        ]
        s.add_roles( s.get_role_adders(*role_tuple_list) )

