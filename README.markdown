# Installation
### User installation:

As Django 1.4 has not been released, it's not yet included as dependencies in `setup.py`. So you need to install it separately.

    mkvirtualenv proteus-deploy-user
    pip install git+git://github.com/Proteus-tech/deploy.git@develop
    pip freeze

If you find `Django==1.4` and `proteus-deploy==0.0.7` in your environment, then everything is good! Now you can start a new project (See Create a project section).

NOTE: If you not have virtualenvwrapper, you can see installation virtualenvwrapper guide [here](https://github.com/Proteus-tech/deploy/wiki/Scenario-of-installation-virtualenvwrapper).

### Development installation:

First, clone the project, then follow the steps below:

    mkvirtualenv --no-site-packages proteus-deploy-dev
    pip install -r setup/requirements.txt
    ./runtests

If all tests pass, you are good to go.

NOTE: If you not have virtualenvwrapper, you can see installation virtualenvwrapper guide [here](https://github.com/Proteus-tech/deploy/wiki/Scenario-of-installation-virtualenvwrapper).

### Create a project
Once you have installed proteus-deploy, you will have startproject command in your environment.

For example, if you want to create a project name `student`.

    startproject student

A Django 1.4 project named student would be created at your current directory.

### Start new simple server without postgres
Starts a new server.

#### Prerequisites
The target region of the server must have 2 security groups prepared (`ssh` and `http`).

Simple step:

    start-simple-server client-name

Full step:

    start-simple-server client-name bits region size ami

Required parameter(s):

- **client-name**

Optional parameter(s):

- **bits** 32 | 64 (default: 64)
- **region** us-west-1, us-west-2 or ap-southeast-1 (default: us-west-1)
- **size** size of the instance (default: t1.micro)
- **ami** an AMI ID that consistent with other parameters (default: ami-4d580408)

### Start new simple server with postgres
Complete Start new simple server without postgres, then follow the steps below:

    pf-server-role-add client-name ec2-host postgres

Required parameter(s):

- **client-name**
- **ec2-host** the public domain of the EC2 instance (i.e ec2-184-169-247-45.us-west-1.compute.amazonaws.com)

### Setup buildbot on an existing server
Setups buildbot on an existing EC2 instance.

#### Prerequisites
The root folder of the repository must contain `buildbot/master.cfg`.

Simple step:

    setup-buildbot-on-server client-name ec2-host repository-url

Full step:

    setup-buildbot-on-server client-name ec2-host project-name repository-url privacy

Required parameter(s):

- **client-name**
- **ec2-host** the public domain of the EC2 instance (i.e ec2-184-169-247-45.us-west-1.compute.amazonaws.com)
- **repository-url**

Optional parameter(s):
- **project-name** the name of the project (default:  project name from repository-url)
- **privacy** repository is public or private (public|private, default: public)

### Setup buildbot with svn on an existing server
Setups buildbot on an existing EC2 instance.

#### Prerequisites
The root folder of the repository must contain `buildbot/master.cfg`.

Simple step:

    setup-buildbot-svn-on-server client-name ec2-host repository-url

Full step:

    setup-buildbot-svn-on-server client-name ec2-host project-name
repository-url privacy

Required parameter(s):

- **client-name**
- **ec2-host** the public domain of the EC2 instance (i.e
ec2-184-169-247-45.us-west-1.compute.amazonaws.com)
- **repository-url**

Optional parameter(s):
- **project-name** the name of the project (default:  project name from
repository-url)
- **privacy** repository is public or private (public|private, default: private)

### Start new buildbot server
Starts a new server and setup buildbot on it.

Simple step:

    start-buildbot-server client-name repository-url

Full step:

    start-buildbot-server client-name project-name repository-url privacy bits region size ami

Required parameter(s):

- **client-name**
- **repository-url**

Optional parameter(s):

- **project-name** the name of the project (default:  project name from repository-url)
- **privacy** repository is public or private (public|private, default: public)
- **bits** 32 | 64 (default: 64)
- **region** us-west-1, us-west-2 or ap-southeast-1 (default: us-west-1)
- **size** size of the instance (default: t1.micro)
- **ami** an AMI ID that consistent with other parameters (default:
ami-4d580408)

### Start new buildbot server for svn repository
Starts a new server and setup buildbot on it.

Simple step:

    start-buildbot-svn-server client-name repository-url

Full step:

    start-buildbot-svn-server client-name project-name repository-url privacy
bits region size ami

Required parameter(s):

- **client-name**
- **repository-url**

Optional parameter(s):

- **project-name** the name of the project (default:  project name from
repository-url)
- **privacy** repository is public or private (public|private, default: private)
- **bits** 32 | 64 (default: 64)
- **region** us-west-1, us-west-2 or ap-southeast-1 (default: us-west-1)
- **size** size of the instance (default: t1.micro)
- **ami** an AMI ID that consistent with other parameters (default:
ami-4d580408)

### Setup buildbot slave on existing server
Setups buildbot slave on an existing EC2 instance.

#### Prerequisites
The buildbot master server must valid and has public doamin ( to be ec2-master-host value ).

##### For git repository
Simple step:

    setup-buildbot-slave-on-server client-name ec2-host ec2-master-host repository-url

Full step:

    setup-buildbot-slave-on-server client-name ec2-host ec2-master-host project-name repository-url privacy

Required parameter(s):

- **client-name**
- **ec2-host** the public domain of the EC2 instance (i.e ec2-184-169-247-45.us-west-1.compute.amazonaws.com)
- **ec2-master-host** the public domain of the buildbot master EC2 instance ( Use "localhost" for same instance )
- **repository-url**

Optional parameter(s):

- **project-name** the name of the project (default:  project name from repository-url)
- **privacy** repository is public or private (public|private, default: public)

##### For svn repository
Simple step:

    setup-buildbot-slave-svn-on-server client-name ec2-host ec2-master-host
repository-url

Full step:

    setup-buildbot-slave-svn-on-server client-name ec2-host ec2-master-host
project-name repository-url privacy

Required parameter(s):

- **client-name**
- **ec2-host** the public domain of the EC2 instance (i.e
ec2-184-169-247-45.us-west-1.compute.amazonaws.com)
- **ec2-master-host** the public domain of the buildbot master EC2 instance (
Use "localhost" for same instance )
- **repository-url**

Optional parameter(s):

- **project-name** the name of the project (default:  project name from
repository-url)
- **privacy** repository is public or private (public|private, default: private)

### Setup postgres buildbot slave on existing server
Setups postgres buildbot slave on an existing EC2 instance.

#### Prerequisites
The buildbot master server must valid and has public doamin ( to be ec2-master-host value ).

#####For git repository
Simple step:

    setup-pg-slave-on-server client-name ec2-host ec2-master-host repository-url

Full step:

    setup-pg-slave-on-server client-name ec2-host ec2-master-host project-name repository-url privacy

#####For svn repository
Simple step:

    setup-pg-slave-on-svn-server client-name ec2-host ec2-master-host repository-url

Full step:

    setup-pg-slave-on-svn-server client-name ec2-host ec2-master-host project-name repository-url

Required parameter(s):

- **client-name**
- **ec2-host** the public domain of the EC2 instance (i.e ec2-184-169-247-45.us-west-1.compute.amazonaws.com)
- **ec2-master-host** the public domain of the buildbot master EC2 instance ( Use "localhost" for same instance )
- **repository-url**

Optional parameter(s):

- **project-name** the name of the project (default:  project name from repository-url)
- **privacy** repository is public or private (public|private, default: public)

### Create postgres slave file for master configuration file for Git repository
Create pg_slave.py in /project_name/buildbot_config/slaves

    add-pg-slave-to-master-cfg

### Create postgres slave file for master configuration file for SVN repository
Create pg_slave.py in /project_name/buildbot_config/slaves

    add-pg-slave-to-master-svn-cfg    
    
### Restarting buildbot
When new `master.cfg` is committed, it would not affect until the buildbot master has been restarted.

To restart master, runs:

    restart-buildbot-master client-name ec2-host project-name

Required parameter(s):

- **client-name**
- **ec2-host** the public domain of the EC2 instance (i.e ec2-184-169-247-45.us-west-1.compute.amazonaws.com)
- **project-name** the name of the project

Occasionally, you might find that restarting master causes the build slaves to hang. Restarting slaves should fix it.

To restart slave, runs:

    restart-buildbot-slave client-name ec2-host project-name

Required parameter(s):

- **client-name**
- **ec2-host** the public domain of the EC2 instance (i.e ec2-184-169-247-45.us-west-1.compute.amazonaws.com)
- **project-name** the name of the project

# Roles

## proteus.buildbot_master

    --proteus.buildbot_master repository,project_name

Setup buildbot master environment according to `master.cfg` in the project. Usually followed by `proteus.start_buildbot_master`.

## proteus.buildbot_slave

    --proteus.buildbot_slave repository,project_name

Setup a build slave of the project. You need to update `master.cfg` to let the master knows this new slave. Usually followed by `proteus.start_buildbot_slave`.

## proteus.buildbot_pg_slave

    --proteus.buildbot_pg_slave repository,ec2-host,project_name
    
Setup a build slave of the project with postgres database.

## proteus.credentials

    --proteus.credentials repository

Do `ssh-keygen` on the machine and add the generated key on repository so that the machine can checkout private code from the repository.

## proteus.restart_buildbot_master

    --proteus.restart_buildbot_master project

Restart buildbot master of the given `project` on the machine.

## proteus.restart_buildbot_slave

    --proteus.restart_buildbot_slave project

Restart buildslave of the given `project` on the machine.

## proteus.start_buildbot_master

    --proteus.start_buildbot_master project

Start buildbot master of the given `project` on the machine.

## proteus.start_buildbot_slave

    --proteus.start_buildbot_slave project[,ec2_master_host]

Start build slave of the given `project` on the machine. If the master is on a different machine `ec2_master_host` needs to be specified.

## proteus.www_home

    proteus.www_home

Set `/home/www-data/` as `$HOME` folder of user `www-data` of the machine (default is `/var/www/`) and also set `bash` as the default shell.

# Folders
## proteus
`proteus` is a package which contains profab roles.

## project template
`project_template` contains a template for creating a project according to standardized layout.


