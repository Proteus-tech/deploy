from buildbot.buildslave import BuildSlave
from buildbot.config import BuilderConfig
from buildbot.schedulers.basic import SingleBranchScheduler
from proteus_buildbot.slaves import sqlite_slave
from unittest import TestCase

class TestSqilteSlave(TestCase):
    def test_scheduler(self):
        self.assertTrue(isinstance(sqlite_slave.scheduler, SingleBranchScheduler))
        self.assertEqual(sqlite_slave.scheduler.builderNames, ['builder-sqlite'])

    def test_builder(self):
        self.assertTrue(isinstance(sqlite_slave.builder, BuilderConfig))
        self.assertEqual(sqlite_slave.builder.name, 'builder-sqlite')
        self.assertEqual(sqlite_slave.builder.slavenames, ['slave1'])

    def test_slave(self):
        self.assertTrue(isinstance(sqlite_slave.slave, BuildSlave))
        self.assertEqual(sqlite_slave.slave.slavename, 'slave1')

