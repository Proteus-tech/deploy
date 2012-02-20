import os
from setuptools import setup

template_dir = 'project_template'
data_files = []
for dirpath, dirnames, filenames in os.walk(template_dir):
    if filenames:
        data_files.append([dirpath, 
            [os.path.join(dirpath, f) for f in filenames]])

setup(
    name = "proteus-deploy",
    version = "0.0.1",
    author = "Proteus Technologies",
    author_email = "dev-team@proteus-tech.com",
    scripts = ["project_template/bin/startproject"],
    data_files = data_files
)
