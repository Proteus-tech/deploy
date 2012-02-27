import sys

from fabric.api import local, run
from fabric.operations import sudo
from fabric.contrib.files import exists

from profab.server import Server

BASE_ROLES = [
    ('security_group','ssh'),
    ('security_group','http'),
    ('postgres',None),
    ('wsgi',None), # Adds the default WSGI configuration , installing apache2, libapache2-mod-wsgi.
]

def simple_server(
    using_client,
    bits='64',
    region='us-west-1',
    ami='ami-4d580408',
    base_roles=BASE_ROLES
):
    '''
    Create simple server : using_client, bits, region, ami
    '''
    role_tuple_list = [
        ('bits',bits),
        ('region',region),
        ('ami',ami),
    ]

    return Server.start(
        using_client,
        *(base_roles + role_tuple_list)
    )    

def create_buildbot( using_client, dest_url, project_name, git_url ):
    '''
    Adding buildbot role : using_client, dest_url, project_name, git_url
    '''
    s = Server.connect( client=using_client, hostname=dest_url )
    if s:
        role_tuple_list = [
            ('proteus.buildbot','%s,%s' % (project_name, git_url) ),
        ]
        s.add_roles( s.get_role_adders(*role_tuple_list) )


