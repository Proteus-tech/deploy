from buildbot.schedulers.basic import SingleBranchScheduler
from proteus_buildbot.slaves import sqlite_slave
from unittest import TestCase

class TestSqilteSlave(TestCase):
    def test_scheduler(self):
        self.assertTrue(isinstance(sqlite_slave.scheduler, SingleBranchScheduler))

