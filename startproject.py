from django.core import management
from subprocess import call
import os, shutil, string, random

def create_project(project_name, template_path):
    template_option = "--template=%s" % template_path
    management.execute_from_command_line(["django-admin.py", "startproject", project_name, template_option])
    

def create_python_package(path):
    os.makedirs(path)
    call(["touch", os.path.join(path, '__init__.py')])

def pythonify(template_path, file_name, src_dir, dst_dir):
    """
    Try to fool django that this is a python file by 
    - moving it into a python library.
    - append .py after file_name

    Parameters:
    - file_name
    - src_dir*, the folder that contains the file
    - dst_dir*, the destination folder 
    
    * src_dir and dst_dir are collection of folder name to os.path.join
    """
    src_dir = src_dir + [file_name]
    dst_dir = dst_dir + [file_name + '.py']
    src = os.path.join(template_path, *src_dir)
    dst = os.path.join(template_path, *dst_dir)
    shutil.move(src, dst)

def unpythonify(project_dir, file_name, src_dir, dst_dir):
    src_dir = src_dir + [file_name + '.py']
    dst_dir = dst_dir + [file_name]
    src = os.path.join(project_dir, *src_dir)
    dst = os.path.join(project_dir, *dst_dir)
    shutil.move(src, dst)
 
def cleanup(project_dir):
    """
    remove build folder and __init__.py in project_dir
    """
    build_root = os.path.join(project_dir, 'build')
    shutil.rmtree(build_root)
    project_init = os.path.join(project_dir, '__init__.py')
    os.remove(project_init)

def chmod_scripts(project_dir):
    scripts = ['runtests', 'runserver', 'reset_db']
    for script in scripts:
        script_path = os.path.join(project_dir, script)
        os.chmod(script_path, 0744)

def move_files_into_build(template_path):
    """
    1. create build and build/buildbot package
    2. pythonify
       - runtests -> build/runtests.py
       - buildbot/master.cfg -> build/buildbot/master.cfg

    When Django is starting project, file *.py which contains 
    {{ project_name }} would be rendered. In order to make others
    scripts such as runtests also be rendered, we need to create
    a temporary `build` package to trick django to render them.
    """
    build_root = os.path.join(template_path, 'build')

    if os.path.exists(build_root):
        return

    create_python_package(build_root)

    build_buildbot = os.path.join(template_path, 'build', 'buildbot')
    create_python_package(build_buildbot)

    pythonify(template_path, 'runtests', [], ['build']) 
    pythonify(template_path, 'reset_db', [], ['build']) 
    pythonify(template_path, 'master.cfg', ['buildbot'], ['build', 'buildbot']) 

def move_files_out_of_build(project_dir):
    unpythonify(project_dir, 'runtests', ['build'], [])
    unpythonify(project_dir, 'reset_db', ['build'], [])
    unpythonify(project_dir, 'master.cfg', ['build', 'buildbot'], ['buildbot'])

def replace_secret_key(path_to_replace):
    tmp_key = [random.choice(string.letters + string.digits) for x in xrange(50)]
    skey = "".join(tmp_key)
    os.system('sed -i \"s/^SECRET_KEY = .*/SECRET_KEY = \'%s\'/g\" %s' % (skey, path_to_replace))

