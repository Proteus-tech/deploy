from buildbot.buildslave import BuildSlave
from buildbot.config import BuilderConfig
from buildbot.process.factory import BuildFactory
from buildbot.steps.shell import ShellCommand

from buildbot_config.settings import BRANCH, PROJECT_NAME, PROJECT_CODE_URL

nickname = 'sqlite'
name = 'slave-%s' % nickname
builder_name = 'builder-%s' % nickname
# slave
slave = BuildSlave(name, "%spassword" % name)
# builder
factory = BuildFactory()
factory.addStep(ShellCommand(command="git pull origin develop", workdir=PROJECT_CODE_URL))
# Pip install and update to environment which run this buildbot
factory.addStep(ShellCommand(command=["pip", "install", "--upgrade", "--requirement=setup/requirements.txt"],workdir=PROJECT_CODE_URL))
factory.addStep(ShellCommand(command=["pip", "freeze"], workdir=PROJECT_CODE_URL))
factory.addStep(ShellCommand(command=["/bin/bash","reset_db"], workdir=PROJECT_CODE_URL))
factory.addStep(ShellCommand(command=["/bin/bash","runtests"], workdir=PROJECT_CODE_URL))

builder = BuilderConfig(name=builder_name
            , slavenames=[name]
            , factory=factory)

