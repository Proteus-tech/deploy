from profab.server import Server

BASE_ROLES = [
    ('security_group','ssh'),
    ('security_group','http'),
    ('postgres',None),
    ('wsgi',None), # Adds the default WSGI configuration , installing apache2, libapache2-mod-wsgi.
]

def start(
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

