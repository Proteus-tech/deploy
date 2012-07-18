from profab.role import Role
from proteus.authorize_key import authorize_key
from proteus.buildbot import split_svn_url
from proteus.ssh_key_gen import ssh_key_gen
from proteus.trust_host import trust_host
from proteus.www_home import www_home

def credentials_svn(server, repository):
    host = split_svn_url(repository)
    www_home(server)
    ssh_key_gen(server)
#    authorize_key(server, repository)
    trust_host(server, host)

class Configure(Role):
    '''
    Combined roles  of ssh_key_gen, proteus.authorize_key and proteus.trust_host
    '''
    def configure(self, server):
        repository = self.parameter 
        credentials_svn(server, repository)

