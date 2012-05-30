from boto.s3.bucket import Bucket
from boto.s3.connection import S3Connection
from fabric.api import local
from fabric.context_managers import cd
from fabric.operations import os ,sudo, get
from profab import Configuration
from profab.role import Role
from proteus import buildbot

def setup(server, bucket_name, s3_location, tar_name, remote_tar_path, client_name):
    local('mkdir -p /home/www-data/buildpackage')
    local_tar_path = '/home/www-data/buildpackage'
    config = Configuration(client_name)
    s3cnx = S3Connection(aws_access_key_id=config.keys.api,
            aws_secret_access_key=config.keys.secret)
    download_tar_from_buildserver(server, remote_tar_path, tar_name, local_tar_path)
    create_bucket_on_s3(bucket_name, s3cnx, s3_location)
    upload_package_to_s3(server, bucket_name, s3cnx, tar_name, local_tar_path)

def create_bucket_on_s3(bucket_name, s3cnx, s3_location):
    bucket_on_server = s3cnx.lookup(bucket_name)
    if bucket_on_server == None:
        try:
            s3cnx.create_bucket(bucket_name=bucket_name, location=s3_location)
        except:
            raise Exception('%s has already in other bucket' % bucket_name)
    else: 
        print '%s has already in your bucket' % bucket_name
 
def upload_package_to_s3(server, bucket_name, s3cnx, tar_name, tar_path):
    keyname = tar_name
    bucket = Bucket(connection=s3cnx, name=bucket_name)
    key = bucket.get_key(keyname)
    if key:
        print key, "already exists"
    else:
        in_path = local('ls %s' % tar_path, capture=True)
        if tar_name in in_path:
            print tar_name, "has already been made"
            print "Uploading", keyname
            key = bucket.new_key(keyname)
            key.set_contents_from_filename('%s/%s' % (tar_path, tar_name))
            local('rm -rf %s' % tar_name)
        else:
            print "Don't have", tar_name

def download_tar_from_buildserver(server, remote_tar_path, tar_name, local_tar_path):
    get('%s/%s' % (remote_tar_path, tar_name), local_tar_path)


class Configure(Role):
    """
    Upload package to bucket on S3  
    parametor
    - bucket_name   name of bucket to create or use
    - s3_location   server's localtion 
    - tar_name      tar file's name to upload to S3
    - remote_tar_path      tar file's  path on buildserver
    - client_name   find from .profab/
    """
    def configure(self, server):
        bucket_name, s3_location, tar_name, remote_tar_path, client_name = buildbot.splitter(self.parameter)
        setup(server, bucket_name, s3_location, tar_name, remote_tar_path, client_name)
