#!/usr/bin/env python
from fabric.context_managers import cd, prefix
from fabric.operations import sudo, run
from fabric.contrib.files import exists, upload_template
from fabric.api import local

from profab.role import Role
from proteus.tag import tag


class AddRole(Role):
    """Create /home/<current-user>/.profab/<client-name>/ec2.json for using with profab.
    """

    def configure(self, server):
        client_name = server.config.client
        current_user = run("whoami").strip()
        user_home_folder = "/home/%s" % current_user
        profab_config_folder = "/%s/.profab/%s" % (user_home_folder, client_name)
        run("mkdir -p %s" % profab_config_folder)
        upload_template("%s/ec2.json" % (profab_config_folder), destination=profab_config_folder)
        tag(server,"profab","installed")
