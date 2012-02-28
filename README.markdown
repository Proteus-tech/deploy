# Installation
User installation:
    As Django 1.4 has not been released, it's not yet included as dependencies in `setup.py`. So you need to install it separately.

    pip install http://www.djangoproject.com/download/1.4-beta-1/tarball/
    pip install git+git://github.com/Proteus-tech/deploy.git@develop
    pip freeze

If you find `Django==1.4b1` and `proteus-deploy==0.0.1` in your environment, then everything is good! Now you can start a new project (See Create a project section).

Development installation:
    First, clone the project, then follow the steps below:

    mkvirtualenv --no-site-packages proteus-deploy
    pip install -r setup/requirements.txt
    ./runtests

If all tests pass, you are good to go.

# Create a project
Once you have installed proteus-deploy, you will have startproject command in your environment.

For example, if you want to create a project name `student`.

    startproject student

A Django 1.4 project named student would be created at your current directory.

# proteus
`proteus` is a package which contains profab roles.

# project template
`project_template` is a template for creating a project according to standardized layout.
