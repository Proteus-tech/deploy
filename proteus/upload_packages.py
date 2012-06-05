#!/usr/bin/env python

from boto.s3.bucket import Bucket
from boto.s3.connection import S3Connection
from fabric.api import local
from fabric.operations import os ,sudo, get
from profab import Configuration
from profab.role import Role
from proteus import buildbot

def upload_package(server, bucket_name, remote_tarfile_path):
    # create folder in buildslave server
    local('mkdir -p /home/www-data/buildpackage')
    local_tar_path = '/home/www-data/buildpackage'

    # get client name from server instance
    config = Configuration(server.config.client)

    # use key from config variable
    s3cnx = S3Connection(
        aws_access_key_id=config.keys.api,
        aws_secret_access_key=config.keys.secret
    )

    # download backup file from build server to buildslave server
    get(remote_tarfile_path, local_tar_path)

    # check on s3 if our bucket_name is valid on there
    if s3cnx.lookup(bucket_name) == None:
        try:
            s3cnx.create_bucket(bucket_name=bucket_name, location=server.cnx.region.name)
        except:
            raise Exception("%s has duplicate name" % bucket_name)
    else:
        print "%s is valid" % bucket_name

    # get tarfile name from tarfile_path
    if remote_tarfile_path.endswith('/'):
        tarfile = remote_tarfile_path.rstrip('/').split('/')[-1]
    else:
        tarfile = remote_tarfile_path.split('/')[-1]

    # connect bucket to get key
    bucket = Bucket(connection=s3cnx, name=bucket_name)
    key = bucket.get_key(tarfile)
    if key:
        print "%s is valid" % tarfile
    else:
        list_items = local("ls %s" % local_tar_path, capture=True)
        if tarfile in list_items:
            print "Start uploading %s" % (tarfile)
            nkey = bucket.new_key(tarfile)
            local_tarfile_path = "%s/%s" % (local_tar_path, tarfile)
            nkey.set_contents_from_filename(
                local_tarfile_path
            )
            local("rm -rf %s" % (local_tar_path))
        else:
            print "%s not found" % tarfile

class Configure(Role):
    """
    Upload package to bucket on S3  
    parameters
        bucket_name : bucket's name
        remote_tarfile_path : full path to tarfile name
    """
    def configure(self, server):
        bucket_name,remote_tarfile_path = buildbot.splitter(self.parameter)
        upload_package(server, bucket_name, remote_tarfile_path)

