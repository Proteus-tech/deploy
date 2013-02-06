from commands import getoutput
from fabric.api import local, put
from fabric.contrib.files import exists
from fabric.operations import sudo
from os import system
from profab.role import Role


def get_server_list(project_name):
    aws_string = getoutput('pf-server-list %s' % project_name)
    return aws_string

def write_file(aws_dict, project_name):
    path_aws = '/tmp/Trac'
    system('mkdir -p %s' % path_aws)
    infile = open('%s/aws_list_%s' % (path_aws, project_name), 'w')
    infile.write(str(aws_dict))
    infile.close()

def read_file(project_name):
    path_aws = '/tmp/Trac'
    outfile = open('%s/aws_list_%s' % (path_aws, project_name), 'r')
    aws_dict = outfile.read()
    return aws_dict

def select_aws_name(aws_string):
    list_tmp = aws_string.split('\n')
    list_aws = []
    for i in range(len(list_tmp)):
        if list_tmp[i].startswith('ec2'): 
            list_aws.append(list_tmp[i])
    return list_aws

def split_detail(aws_list):
    aws_detail = {}
    aws_detail_list = []
    for i in range(len(aws_list)):
        aws_dns = aws_list[i].split(' -- ')[0]
        aws_status = aws_list[i].split(' -- ')[1].split(' ')[0]
        aws_detail['dns'] = aws_dns
        aws_detail['status'] = aws_status
        aws_detail['pub_ip'] = aws_dns.split('ec2-')[1].split('.')[0]
        aws_detail_list.append(str(aws_detail))
    return aws_detail_list

def get_all_attibutes(server, aws_ip):
    aws_attr = []
    reservations = server.instance.connection.get_all_instances()
    instances = [i for r in reservations for i in r.instances]
    for i in instances:
        aws_attr.append(i.__dict__)
        break
    return aws_attr

def put_update_to_trac_server(server, aws_list, project_name):
    current_user = 'ubuntu'
    path_on_client = '/tmp/Trac'
    path_on_server = '/home/%s/Trac/aws-update/%s' % (current_user, project_name)
    if not exists(path_on_server):
        sudo('mkdir -p %s' % path_on_server, user=current_user)
    put('%s/aws_list_%s' % (path_on_client, project_name), '%s/' % path_on_server)
        

class Configure(Role):
    
    def configure(self, server):
        project_name = self.parameter
        aws_list = get_server_list(project_name)
        aws_detail = select_aws_name(aws_list)
        aws_dict = split_detail(aws_detail)
        write_file(aws_dict, project_name)
        aws_details = read_file(project_name)
        put_update_to_trac_server(server, aws_details, project_name)

