from subprocess import call
import os, shutil

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

