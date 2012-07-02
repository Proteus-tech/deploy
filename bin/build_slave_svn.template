from buildbot.buildslave import BuildSlave
from buildbot.config import BuilderConfig
from buildbot.process.factory import BuildFactory
from buildbot.steps.shell import ShellCommand, SetProperty


from buildbot_config.settings import BRANCH, PROJECT_NAME, PROJECT_CODE_URL,REPOSITORY_URL
svn_username = 'www-data'
svn_password = 'www-d@t@!@#'
nickname = 'build'
name = 'slave-%s' % nickname
builder_name = 'builder-%s' % nickname
# slave
slave = BuildSlave(name, "%spassword" % name)
# builder

import re
def get_ip_bb(rc, stdout, stderr):
    ip_server = None
    if stdout:
        ip_server = stdout.split(' ')[0]
        ip_server = ip_server.lstrip('[')
        ip_server = ip_server.rstrip(']')
        match = re.search(r'ec2-(\d+)-(\d+)-(\d+)-(\d+).', ip_server)
        ip_server = "%s.%s.%s.%s" % (match.group(1), match.group(2), match.group(3), match.group(4))
    return {"ec2_ip":ip_server}

from buildbot.steps.shell import WithProperties

DEPLOY_SRC_DIR = '/home/www-data/Buildbot/%s/deploy' % (PROJECT_NAME)
CLIENT_NAME = 'proteus'
DEPLOY_GIT_URL = 'git://github.com/Proteus-tech/deploy.git'

factory = BuildFactory()
factory.addStep(
    SetProperty(
        command=[
            'start-simple-server',
            CLIENT_NAME
        ],
        workdir=PROJECT_CODE_URL,
        extract_fn=get_ip_bb,
    )
)

REPO = REPOSITORY_URL.rstrip('/')

factory.addStep(
    ShellCommand(
        command=[
            'pf-server-role-add',
            CLIENT_NAME,
            WithProperties('%s','ec2_ip'),
            '--proteus.svn_build_checkout',
            REPO
        ],
        env={'PYTHONPATH':'.'},
        workdir=DEPLOY_SRC_DIR,
        description=['checkout sourcecode']
    )
)

factory.addStep(
    ShellCommand(
        command=[
            'pf-server-role-add',
            CLIENT_NAME,
            WithProperties('%s','ec2_ip'),
            '--proteus.create_build_package_svn',
            '%s,%s' % (DEPLOY_GIT_URL,REPO)
        ],
        env={'PYTHONPATH':'.'},
        workdir=DEPLOY_SRC_DIR,
        description=['create build package']
    )
)
factory.addStep(
    ShellCommand(
        command=[
            'pf-server-terminate',
            CLIENT_NAME,
            WithProperties('%s','ec2_ip')
        ],
        workdir=PROJECT_CODE_URL,
        description=['Terminate EC2Instance']
    )
)


builder = BuilderConfig(name=builder_name
    , slavenames=[name]
    , factory=factory)

