from setuptools import setup

setup(
    name = 'proteus-deploy',
    version = '0.0.7',
    author = 'Proteus Technologies',
    author_email = 'dev-team@proteus-tech.com',
    zip_safe = False, # for project_template
    scripts = ['bin/startproject'
        , 'bin/start-simple-server'
        , 'bin/start-buildbot-server'
        , 'bin/setup-buildbot-on-server'
        , 'bin/setup-buildbot-slave-on-server'
        , 'bin/restart-buildbot-master'
        , 'bin/complete_master_config'
        , 'bin/restart-buildbot-slave' 
        , 'bin/add-pg-slave-to-master-cfg'
        , 'bin/setup-pg-slave-on-server'

    ],
    packages = ['project_template'
        , 'project_template.buildbot_config'
        , 'project_template.buildbot_config.slaves'
        , 'project_template.project_name'
        , 'project_template.project_name.tests'
        , 'project_template.project_name_project'
        , 'project_template.project_name_project.settings'
        , 'project_template.buildbot_config.slaves_svn'
        , 'proteus'
        , '.'
    ],
    package_data = {
        'project_template': ['setup/*'
            , 'buildbot_config/master.cfg'
            , 'buildbot_config/master_svn.cfg'
            , 'runtests'
            , 'runserver'
            , 'reset_db' 
        ],
    },
    install_requires = [
        'profab',
        'django'
    ],
)
