from unittest import TestCase
from project_template.project_name_project import settings
from project_template.bin.startproject import create_python_package, pythonify
import os, shutil

class TestStartProjectScript(TestCase):
    """
    bin/startproject
    """
    def tearDown(self):
        if os.path.exists('teddy'):
            shutil.rmtree('teddy')

    def test_create_python_package(self):
        # Act
        create_python_package('teddy') 
        # Assert
        self.assertTrue(os.path.exists('teddy'))
        self.assertTrue(os.path.exists('teddy/__init__.py'))

    def test_pythonify(self):
        # Arrange
        shutil.copyfile('tests/sample_file_to_pythonify', 
                        'tests/sample_file_to_pythonify.tmp')
        self.test_create_python_package() # create teddy
        template_path = '.'
        file_name = 'sample_file_to_pythonify.tmp'
        source = ['tests']
        destination = ['teddy']
        pythonify(template_path, file_name, source, destination)
        
        
class TestTransactionMiddleWare(TestCase):
    def test_transaction_middleware_exist(self):
        """
        TransactionMiddleware should be included by default

        We should use transaction middleware by default to avoid dealing
        with transaction problem later on when a project needs it.
        """
        self.assertTrue('django.middleware.transaction.TransactionMiddleware' in
                        settings.MIDDLEWARE_CLASSES)
        
