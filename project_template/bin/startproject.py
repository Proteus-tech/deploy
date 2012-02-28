from django.core import management
from subprocess import call
import os, shutil

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

