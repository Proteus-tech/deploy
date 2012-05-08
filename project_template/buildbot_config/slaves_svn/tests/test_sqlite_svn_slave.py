from buildbot.buildslave import BuildSlave
from buildbot.config import BuilderConfig
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot_config.slaves import sqlite_slave
from unittest import TestCase

class TestSqilteSvnSlave(TestCase):
    def test_builder_name(self):
        self.assertEqual(sqlite_svn_slave.builder_name, 'builder-sqlite')

    def test_builder(self):
        self.assertTrue(isinstance(sqlite_svn_slave.builder, BuilderConfig))
        self.assertEqual(sqlite_svn_slave.builder.name, 'builder-sqlite')
        self.assertEqual(sqlite_svn_slave.builder.slavenames, ['slave-sqlite'])

    def test_slave(self):
        self.assertTrue(isinstance(sqlite_svn_slave.slave, BuildSlave))
        self.assertEqual(sqlite_svn_slave.slave.slavename, 'slave-sqlite')

