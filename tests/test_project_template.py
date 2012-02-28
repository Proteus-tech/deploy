from project_template.project_name_project import settings
from project_template.bin.startproject import (create_python_package, pythonify,
    unpythonify, create_project, cleanup, chmod_scripts)

from subprocess import call

from unittest import TestCase

import os, shutil, stat

class TestStartProjectScript(TestCase):
    """
    bin/startproject
    """
    def tearDown(self):
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('teddy'):
            shutil.rmtree('teddy')
        if os.path.exists('sample_project'):
            shutil.rmtree('sample_project')
        if os.path.exists('tests/sample_file_to_pythonify.tmp'):
            os.remove('tests/sample_file_to_pythonify.tmp')

    def test_create_python_package(self):
        # Act
        create_python_package('build') 
        # Assert
        self.assertTrue(os.path.exists('build'))
        self.assertTrue(os.path.exists('build/__init__.py'))

    def test_pythonify(self):
        """
        Scenario: 
        1. clone tests/sample_file_to_pythonify (avoid the test screwing it up)
        2. create build package
        3. pythonify the cloned file into the package
        Expected:
        - the cloned file is moved into the package
        - .py is appended in the cloned file's name
        - the content in the file still ok
        """
        # Arrange
        shutil.copyfile('tests/sample_file_to_pythonify', 
                        'tests/sample_file_to_pythonify.tmp')
        self.test_create_python_package() # create build
        template_path = '.'
        file_name = 'sample_file_to_pythonify.tmp'
        source = ['tests']
        destination = ['build']
        # Act
        pythonify(template_path, file_name, source, destination)
        # Assert
        try:
            with open('build/sample_file_to_pythonify.tmp.py') as stream:
                content = stream.read()
                # check that {{ project_name }} is not missing after copied
                self.assertIn('{{ project_name }}', content)
        except IOError:
            self.fail('build/sample_file_to_pythonify.tmp.py not found')
        
    def test_unpythonify(self):
        # Arrange
        self.test_pythonify() # pythonify sample_file_to_pythonify.tmp
        project_dir = '.'
        file_name = 'sample_file_to_pythonify.tmp'
        source = ['build']
        destination = ['tests']
        # Act
        unpythonify(project_dir, file_name, source, destination) 
        try:
            with open('tests/sample_file_to_pythonify.tmp') as stream:
                pass # This should not raise
        except IOError:
            self.fail('tests/sample_file_to_pythonify.tmp not found')

    def test_create_project(self):
        """
        Scenario:
        1. pythonify tests/sample_file_to_pythonify (results in 
           build/sample_file_to_pythonify.tmp.py)
        2. create project named teddy using the build package as a template
        Expected:
        - {{ project_name }} in teddy/sample_file_to_pythonify.tmp.py is 
          rendered as teddy (due to Django template capability)
        """
        self.test_pythonify()
        create_project('teddy', 'build')
        with open('teddy/sample_file_to_pythonify.tmp.py') as stream:
            content = stream.read()
            self.assertIn('teddy', content)
            self.assertFalse('{{ project_name }}' in content)

    def test_cleanup(self):
        create_python_package('sample_project')
        os.makedirs('sample_project/build')
        cleanup('sample_project')
        self.assertFalse(os.path.exists('sample_project/build'))
        self.assertFalse(os.path.exists('sample_project/__init__.py'))

    def test_chmod_scripts(self):
        # Arrange
        os.makedirs('sample_project')
        call(["touch", 'sample_project/runserver'])
        call(["touch", 'sample_project/runtests'])
        call(["touch", 'sample_project/reset_db'])
        # Act
        chmod_scripts('sample_project')
        # Assert
        owner_can_execute = stat.S_IXUSR
        st = os.stat('sample_project/runserver')
        self.assertTrue(st.st_mode & owner_can_execute)
        st = os.stat('sample_project/runtests')
        self.assertTrue(st.st_mode & owner_can_execute)
        st = os.stat('sample_project/reset_db')
        self.assertTrue(st.st_mode & owner_can_execute)
        

class TestTransactionMiddleWare(TestCase):
    def test_transaction_middleware_exist(self):
        """
        TransactionMiddleware should be included by default

        We should use transaction middleware by default to avoid dealing
        with transaction problem later on when a project needs it.
        """
        self.assertTrue('django.middleware.transaction.TransactionMiddleware' in
                        settings.MIDDLEWARE_CLASSES)
        
