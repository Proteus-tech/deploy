from profab.role import Role
from proteus import buildbot

def tag(server, key, value):
    server.cnx.create_tags([server.instance.id], {key:value})
 
class Configure(Role):
    def configure(self, server):
        '''
        put tag and value on the server with parameters "key,value"
        '''
        key, value = buildbot.splitter(self.parameter)
        tag(server, key, value)
 
