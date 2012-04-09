from buildbot.changes import filter
from buildbot.schedulers.basic import SingleBranchScheduler
from settings import BRANCH, PROJECT_NAME

change_filter = filter.ChangeFilter(project=PROJECT_NAME, branch=BRANCH)

scheduler = SingleBranchScheduler(name="develop-change"
                                , change_filter = change_filter 
                                , treeStableTimer=30
                                , builderNames=["builder-sqlite"])

