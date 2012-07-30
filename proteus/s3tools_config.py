#!/usr/bin/env python

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
    upload_template(
        "templates/s3cfg",
        REMOTE_TARGET,
        use_sudo=True,
        mode=0666
    )
    sed(REMOTE_TARGET, "ACCESS_KEY",client_config.keys.api, use_sudo=True)
    sed(REMOTE_TARGET,"SECRET_KEY",client_config.keys.secret, use_sudo=True)
    sudo("chown -R %s:%s %s" % (remote_user, remote_user, REMOTE_TARGET))


class AddRole(Role):
    """Upload s3cfg to remote host
    """

    def configure(self, server):
        s3tools_config(server)
        tag(server,"s3tools","installed")
