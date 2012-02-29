from setuptools import setup

setup(
    name = 'proteus-deploy',
    version = '0.0.3',
    author = 'Proteus Technologies',
    author_email = 'dev-team@proteus-tech.com',
    zip_safe = False, # for project_template
    scripts = ['bin/startproject'
        , 'bin/start-simple-server'
        , 'bin/setup-buildbot-on-server'
    ],
    packages = ['project_template'
        , 'project_template.project_name'
        , 'project_template.project_name.tests'
        , 'project_template.project_name_project'
        , 'project_template.project_name_project.settings'
        , 'proteus'
        , '.'
    ],
    package_data = {
        'project_template': ['setup/*'
            , 'buildbot/*'
            , 'runtests'
            , 'runserver'
            , 'reset_db' 
        ],
    },
    install_requires = [
        'profab'
    ],
)
