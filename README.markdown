# Installation
### User installation:

As Django 1.4 has not been released, it's not yet included as dependencies in `setup.py`. So you need to install it separately.

    pip install git+git://github.com/Proteus-tech/deploy.git@develop
    pip freeze

If you find `Django==1.4b1` and `proteus-deploy==0.0.1` in your environment, then everything is good! Now you can start a new project (See Create a project section).

### Development installation:

First, clone the project, then follow the steps below:

    mkvirtualenv --no-site-packages proteus-deploy
    pip install -r setup/requirements.txt
    ./runtests

If all tests pass, you are good to go.

### Create a project
Once you have installed proteus-deploy, you will have startproject command in your environment.

For example, if you want to create a project name `student`.

    startproject student

A Django 1.4 project named student would be created at your current directory.

### Start new simple server
Starts a new server.

#### Prerequisites
The target region of the server must have 2 security groups prepared (`ssh` and `http`).

    start-simple-server client-name bits region size ami

Required parameter(s):

- **client-name**

Optional parameter(s):

- **bits** 32 | 64 (default: 64)
- **region** us-west-1, us-west-2 or ap-southeast-1 (default: us-west-1)
- **size** size of the instance (default: t1.micro)
- **ami** an AMI ID that consistent with other parameters (default: ami-4d580408)

### Setup buildbot on an existing server
Setups buildbot on an existing EC2 instance.

#### Prerequisites
The root folder of the repository must contain `buildbot/master.cfg`.

    setup-buildbot-on-server client-name ec2-host project-name repository-url privacy

Required parameter(s):

- **client-name**
- **ec2-host** the public domain of the EC2 instance (i.e ec2-184-169-247-45.us-west-1.compute.amazonaws.com)
- **project-name** the name of the project
- **repository-url**

Optional parameter(s):

- **privacy** repository is public or private (public|private, default: public)

### Start new buildbot server
Starts a new server and setup buildbot on it.

    start-buildbot-server client-name project-name repository-url privacy bits region size ami

Required parameter(s):

- **client-name**
- **project-name** the name of the project
- **repository-url**

Optional parameter(s):

- **privacy** repository is public or private (public|private, default: public)
- **bits** 32 | 64 (default: 64)
- **region** us-west-1, us-west-2 or ap-southeast-1 (default: us-west-1)
- **size** size of the instance (default: t1.micro)
- **ami** an AMI ID that consistent with other parameters (default: ami-4d580408)

##### proteus
`proteus` is a package which contains profab roles.

##### project template
`project_template` contains a template for creating a project according to standardized layout.
