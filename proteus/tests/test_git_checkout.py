from proteus.git_checkout import root_folder
from unittest import TestCase

class TestRootFolder(TestCase):
    def test_root_folder_for_git_readoly_url(self):
        git_url = 'git://github.com/Proteus-tech/deploy.git'
        folder = root_folder(git_url)
        self.assertEqual('deploy', folder)

    def test_root_folder_for_git_http_url(self):
        git_url = 'https://vernomcrp@github.com/Proteus-tech/deploy.git'
        folder = root_folder(git_url)
        self.assertEqual('deploy', folder)

    def test_root_folder_for_git_ssh_url(self):
        git_url = 'git@github.com:Proteus-tech/deploy.git'
        folder = root_folder(git_url)
        self.assertEqual('deploy', folder)
