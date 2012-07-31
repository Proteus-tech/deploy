#!/usr/bin/env python

import os
import sys

from fabric.operations import sudo
from fabric.contrib.files import upload_template, sed

from profab import Configuration
from profab.role import Role
from proteus.tag import tag
from profab import _logger

def s3tools_config(server, remote_user="www-data"):
    client_name = server.config.client
    client_config = Configuration(client_name)
    REMOTE_TARGET = "/home/%s/.s3cfg" % remote_user

    local_template_dir = None
    for path, dirs, files in os.walk(sys.prefix):
        if ('templates' in path) and ('s3cfg' in files):
            local_template_dir = '%s/s3cfg' % path
            _logger.info("found s3cfg at %s ", local_template_dir)
    if local_template_dir is not None:
        upload_template(
            local_template_dir,
            REMOTE_TARGET,
            use_sudo=True,
            mode=0666
        )
        sed(REMOTE_TARGET, "ACCESS_KEY",client_config.keys.api, use_sudo=True)
        sed(REMOTE_TARGET,"SECRET_KEY",client_config.keys.secret, use_sudo=True)
        sudo("chown -R %s:%s %s" % (remote_user, remote_user, REMOTE_TARGET))
        sudo("chown -R %s:%s %s.bak" % (remote_user, remote_user, REMOTE_TARGET))
        _logger.info("upload s3cfg complete.")
    else:
        _logger.warning("upload s3cfg does not complete because s3cfg is not found.")


class AddRole(Role):
    """Upload s3cfg to remote host, setup s3cmd to remote host.
    """
    packages = ['s3cmd']

    def configure(self, server):
        s3tools_config(server)
        tag(server,"s3tools","installed")
