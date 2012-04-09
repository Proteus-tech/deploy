from buildbot.schedulers.basic import SingleBranchScheduler
from project_template.buildbot.proteus import sqlite_slave
from unittest import TestCase

class TestSqilteSlave(TestCase):
    def test_scheduler(self):
        self.assertTrue(isinstance(sqlite_slave.scheduler, SingleBranchScheduler))

