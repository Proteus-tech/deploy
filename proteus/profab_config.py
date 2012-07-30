#!/usr/bin/env python
from fabric.context_managers import cd
from fabric.operations import sudo, run, local
from fabric.contrib.files import exists, upload_template

from profab.role import Role
from proteus.tag import tag
from profab import _logger

def profab_config(server, remote_user="www-data"):
    client_name = server.config.client
    current_user = local("echo $USER", capture=True).strip()
    current_user = 'siraset'
    _logger.info(current_user)
    _logger.info(type(current_user))

    user_home_folder = "/home/%s" % (current_user)
    local_profab_config_folder = "%s/.profab/%s" % (user_home_folder, client_name)

    remote_user_home_folder = "/home/%s" % (remote_user)
    remote_profab_config_folder = "%s/.profab/%s" % (remote_user_home_folder, client_name)

    _logger.info("Checking current_user found [%s]", current_user)
    _logger.info("Construct text %s", local_profab_config_folder)

    sudo("mkdir -p %s" % remote_profab_config_folder, user=remote_user)
    local_ec2_json_path = "%s/ec2.json" % local_profab_config_folder
    _logger.info("Trying to upload %s", local_ec2_json_path )
    upload_template(
        local_ec2_json_path,
        destination=remote_profab_config_folder,
        use_sudo=True,
        mode=0666
    )
    sudo("chown -R %s:%s %s" % (remote_user, remote_user, remote_profab_config_folder))


class AddRole(Role):
    """Create /home/<current-user>/.profab/<client-name>/ec2.json for using with profab.
    """

    def configure(self, server):
        profab_config(server)
        tag(server,"proteus-deploy","installed")
