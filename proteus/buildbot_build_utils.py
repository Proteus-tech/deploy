from fabric.operations import sudo, run
from fabric.context_managers import prefix, cd
from fabric.contrib.files import exists, upload_template

def create_virtenv(server, project_name):
    sudo("easy_install virtualenv")
    project_base_dir = "/home/www-data/%s" % (project_name)
    current_dir = "%s/current" % (project_base_dir)
    with cd(current_dir):
        sudo("virtualenv --no-site-packages virtualenv", user="www-data")
        with prefix("source virtualenv/bin/activate"):
            sudo("pip install -r service/setup/requirements.txt", user="www-data")
            #sudo("pip install -r current/service/setup/server.pip", user="www-data")
            sudo("virtualenv --relocatable virtualenv", user="www-data")

def collect_static(server, project_name):
    project_base_dir = "/home/www-data/%s" % (project_name)
    current_base_dir = "%s/current" % (project_base_dir)
    service_base_dir = "%s/service" % (current_base_dir)
    project_settings_dir = '%s_project' % (project_name)
    upload_template("utilities/build_settings.py", destination=service_base_dir,context={'project_name':project_settings_dir}, use_sudo=True)
    with cd(service_base_dir):
        sudo("chown www-data:www-data build_settings.py")
    with cd(current_base_dir):
        with prefix("source virtualenv/bin/activate"):
            sudo("python service/manage.py collectstatic --noinput --settings=build_settings", user="www-data")

def checkout_deploy_sourcecode(server, project_name, deploy_url, branch="develop"):
    _logger.info('checkout deploy sourcecode on remote machine')
    project_base_folder = "/home/www-data/%s" % (project_name)
    deploy_base_folder = "deploy"
    with cd(project_base_folder):
        if not exists(deploy_base_folder):
            sudo("git clone -q %s %s" % (deploy_url, deploy_base_folder), user="www-data")
            with cd(deploy_base_folder):
                sudo("git checkout -b %s" % (branch), user="www-data")
                sudo("git pull origin %s" % (branch), user="www-data")
                sudo("git checkout %s" % (branch), user="www-data")

def create_tar_file(server, project_name, tarfile_name):
    project_base_dir = "/home/www-data/%s" % (project_name)
    current_dir = "%s/current" % (project_base_dir)
    with cd(current_dir):
        sudo("tar cfa %s service static virtualenv" % (tarfile_name), user='www-data')
        path_to_tarfile = '%s/%s' % (current_dir, tarfile_name)
        return path_to_tarfile

def get_machine_spec(server):
    ubuntu_version = run('lsb_release -cs').strip()
    bits = run('uname -m').strip()
    return (ubuntu_version, bits)