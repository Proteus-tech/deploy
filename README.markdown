# Installation
As Django 1.4 has not been released, it's not yet put in dependencies in `setup.py`.
## Create Virtual Environment
    mkvirtualenv --no-site-packages proteus-deploy

## Install dependency packages
    pip install -r setup/requirements.txt

## Install Proteus-deployment
    pip install git+git://github.com/Proteus-tech/deploy.git@develop

## Check pip freeze
Check `pip freeze` and you should find `Django==1.4b1` and `proteus-deploy==0.0.1` in your environment
    pip freeze
    
# Create a project
Once you have installed proteus-deploy, you will have startproject command in your environment.

For example, if you want to create a project name `student`.

    startproject student

A Django 1.4 project named student would be created at your current directory.

# proteus
`proteus` is a package which contains profab roles.

# project template
`project_template` is a template for creating a project according to standardized layout.
