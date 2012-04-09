from proteus_buildbot.utils import list_modules, module_name
from unittest import TestCase

class TestUtils(TestCase):
    def test_list_modules_with_slaves(self):
        slaves = __import__('proteus_buildbot.slaves', fromlist=['proteus_buildbot', 'slaves'])
        sub_modules = list_modules(slaves) 
        self.assertTrue('sqlite_slave' in sub_modules)
        self.assertTrue('__init__' not in sub_modules)

    def test_list_modules_with_proteus(self):
        proteus = __import__('proteus')
        sub_modules = list_modules(proteus) 
        self.assertTrue('buildbot' in sub_modules)
        self.assertTrue('buildbot_master' in sub_modules)
        self.assertTrue('check_config' in sub_modules)
        self.assertTrue('complete_master_config' in sub_modules)
        self.assertTrue('create_symlink' in sub_modules)
        self.assertTrue('git_checkout' in sub_modules)
        self.assertTrue('setup_buildbot_master' in sub_modules)
        self.assertTrue('tag' in sub_modules)

    def test_module_name_for_dot_py(self):
        module = 'sqlite_slave.py'
        result = module_name(module)
        self.assertEqual('sqlite_slave', result)

    def test_module_name_for_dot_pyc(self):
        module = 'sqlite_slave.pyc'
        result = module_name(module)
        self.assertEqual('sqlite_slave', result)

    def test_module_name_for_dot_swp(self):
        module = 'sqlite_slave.py.swp'
        result = module_name(module)
        self.assertEqual(None, result)

    def test_module_name_for_package(self):
        module = 'tests'
        result = module_name(module)
        self.assertEqual('tests', result)

