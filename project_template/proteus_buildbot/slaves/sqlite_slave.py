from buildbot.buildslave import BuildSlave
from buildbot.changes import filter
from buildbot.config import BuilderConfig
from buildbot.process.factory import BuildFactory
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.steps.shell import ShellCommand

from proteus_buildbot.settings import BRANCH, PROJECT_NAME, PROJECT_CODE_URL

# slave
slave = BuildSlave("slave1", "slave1password")
# scheduler
change_filter = filter.ChangeFilter(project=PROJECT_NAME, branch=BRANCH)
scheduler = SingleBranchScheduler(name="develop-change"
                                , change_filter = change_filter 
                                , treeStableTimer=30
                                , builderNames=["builder-sqlite"])
# builder
factory = BuildFactory()
factory.addStep(ShellCommand(command="git pull origin develop", workdir=PROJECT_CODE_URL))
# Pip install and update to environment which run this buildbot
factory.addStep(ShellCommand(command=["pip", "install", "--upgrade", "--requirement=setup/requirements.txt"],workdir=PROJECT_CODE_URL))
factory.addStep(ShellCommand(command=["pip", "freeze"], workdir=PROJECT_CODE_URL))
factory.addStep(ShellCommand(command=["/bin/bash","reset_db"], workdir=PROJECT_CODE_URL))
factory.addStep(ShellCommand(command=["/bin/bash","runtests"], workdir=PROJECT_CODE_URL))

builder = BuilderConfig(name="builder-sqlite"
            , slavenames=["slave1"]
            , factory=factory)

