import os
from setuptools import setup

setup(
    name = 'proteus-deploy',
    version = '0.0.1',
    author = 'Proteus Technologies',
    author_email = 'dev-team@proteus-tech.com',
    scripts = ['project_template/bin/startproject'],
    packages = ['project_template'
        , 'project_template.project_name'
        , 'project_template.project_name.tests'
        , 'project_template.project_name_project'
        , 'project_template.project_name_project.settings'
    ],
    package_data = {
        'project_template': ['setup/*'
            ,'buildbot/*'
            ,'runtests'
            ,'runserver'
            ,'reset_db' 
        ],
    }
)
