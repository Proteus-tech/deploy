from fabric.operations import sudo
from fabric.contrib.files import exists, sed
from profab.role import Role

def replace_in_file(server, pg_hba_path):
    sed('%s/main/pg_hba.conf' % pg_hba_path
        , '# If you want to allow non-local connections, you need to add more'
        , 'local   all all             trust'
        , use_sudo=True)

    sed('%s/main/pg_hba.conf' % pg_hba_path
        , '# "host" records. In that case you will also need to make PostgreSQL listen'
        , 'host    all all     127.0.0.1/32    md5'
        , use_sudo=True)

    sudo('/etc/init.d/postgresql restart')

def select_postgres_version(server):
    if exists('/etc/postgresql/9.1'):
        replace_in_file(server, '/etc/postgresql/9.1')
    elif exists('/etc/postgresql/8.4'):
        replace_in_file(server, '/etc/postgresql/8.4')
    else:
        msg = '''[Error] Support  postgres version 8.4 and 9.1 only. '''
        raise Exception(msg)

class AddRole(Role):
    '''
    Replace pg_hba.conf on server
    '''
    def configure(self, server):
        select_postgres_version(server)
