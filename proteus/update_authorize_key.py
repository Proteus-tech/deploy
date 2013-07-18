from fabric.operations import sudo
from profab.role import Role

def clean_n_complete(server):
    sudo('''rm -rf /etc/cron.d/replace_key''')
    sudo('''/etc/init.d/cron restart''')
    sudo('''rm -rf /home/ubuntu/replace_key''')
    sudo('''rm -rf /home/ubuntu/.ssh/authorized_keys_new''')

def create_cron(server):
    command = ('0-59 * * * *'
        ' ubuntu cp /home/ubuntu/.ssh/authorized_keys_new'
        ' /home/ubuntu/.ssh/authorized_keys')
    sudo('''echo "%s" > /home/ubuntu/replace_key''' % command)
    sudo('''ln -s /home/ubuntu/replace_key /etc/cron.d/''')
    sudo('''chown root:root /home/ubuntu/replace_key''')
    sudo('''/etc/init.d/cron restart''')

def read_file(path_to_key):
    outfile = open('%s' % path_to_key, 'r')
    return outfile.read()

def update_authorize_key(server, keys):
    create_cron(server)
    sudo('''echo "%s" > /home/ubuntu/.ssh/authorized_keys_new''' 
        % keys, user='ubuntu')
    sudo('''cp /home/ubuntu/.ssh/authorized_keys_new''' 
        ''' /home/ubuntu/.ssh/authorized_keys''')
    clean_n_complete(server)

class Configure(Role):
    def configure(self, server):
        '''
        replace public key from client to the EC2 host
        '''
        path_to_key = self.parameter
        keys = read_file(path_to_key)
        update_authorize_key(server, keys)
