from profab.role import Role
from proteus import buildbot

class Configure(Role):
    def configure(self, server):
        '''
        put tag and value on the server with parameters "key,value"
        '''
        key, value = buildbot.splitter(self.parameter)
        server.cnx.create_tags([server.instance.id], {key:value})
 
