#!/usr/bin/env python
from proteus.create_build_package_git import _get_project_name
from unittest import TestCase

class TestBuildPackage(TestCase):
    def test_get_project_name1(self):
        git_url = 'ssh://git@zeppelin:222/home/git/playable_admin_service/'
        project_name = _get_project_name(git_url)
        self.assertEqual('playable_admin_service',project_name)

    def test_get_project_name2(self):
        git_url = 'ssh://git@zeppelin:222/home/git/playable'
        project_name = _get_project_name(git_url)
        self.assertEqual('playable',project_name)
 
    def test_get_project_name3(self):
        git_url = 'git@github.com:Proteus-tech/deploy.git/'
        project_name = _get_project_name(git_url)
        self.assertEqual('deploy',project_name)

    def test_get_project_name4(self):
        git_url = 'git@github.com:Proteus-tech/deploy.git'
        project_name = _get_project_name(git_url)
        self.assertEqual('deploy',project_name)
 
