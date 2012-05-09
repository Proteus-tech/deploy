from proteus.svn_checkout import root_folder
from unittest import TestCase

class TestRootFolder(TestCase):
    def test_root_folder_for_svn_url_1(self):
        svn_url = 'http://vcs.vps.shogunvps.com:8081/scm-webapp-1.14/svn/testsvn/project/trunk'
        folder = root_folder(svn_url)
        self.assertEqual('project', folder)

    def test_root_folder_for_svn_url_2(self):
        svn_url = 'http://internal.rcis.ac.th/svn/lazypeople/trunk'
        folder = root_folder(svn_url)
        self.assertEqual('lazypeople', folder)

