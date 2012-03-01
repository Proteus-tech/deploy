from startproject import (create_python_package, pythonify,
    unpythonify, create_project, cleanup, chmod_scripts, move_files_into_build, 
    move_files_out_of_build)

from subprocess import call

from unittest import TestCase

import os, project_template, shutil, stat

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

    def test_project_template_module(self):
        msg = """
        project_template needs to be a module or the startproject script
        would not work as it uses project_template.__path__ to find the
        template location

        Don't worry about the created project, the cleanup step would
        removes the __init__.py from the project after created
        """
        self.assertTrue(os.path.isfile('project_template/__init__.py'), msg)

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

    def test_move_files_into_build(self):
        """
        Scenario:
        1. create sample project which contains: 
           - runtests
           - reset_db
           - buildbot/master.cfg
        2. move files in sample project into build
        3. startproject using the sample project as template
        4. move files in created project out of build
        Expected:
        - runtests is rendered
        - reset_db is rendered
        - buildbot/master.cfg is rendered
        """
        # Arrange
        os.makedirs('sample_project')
        os.makedirs('sample_project/buildbot')
        shutil.copyfile('tests/sample_file_to_pythonify', 
                        'sample_project/runtests')
        shutil.copyfile('tests/sample_file_to_pythonify', 
                        'sample_project/reset_db')
        shutil.copyfile('tests/sample_file_to_pythonify', 
                        'sample_project/buildbot/master.cfg')
        # Act
        move_files_into_build('sample_project')
        create_project('teddy', 'sample_project')
        move_files_out_of_build('teddy')
        # Assert
        try:
            with open('teddy/runtests') as stream:
                content = stream.read()
                self.assertIn('teddy', content, 'teddy not found in runtests')
                self.assertFalse('{{ project_name }}' in content)
            with open('teddy/reset_db') as stream:
                content = stream.read()
                self.assertIn('teddy', content, 'teddy not found in reset_db')
                self.assertFalse('{{ project_name }}' in content)
            with open('teddy/buildbot/master.cfg') as stream:
                content = stream.read()
                self.assertIn('teddy', content, 'teddy not found in master.cfg')
                self.assertFalse('{{ project_name }}' in content)
        except IOError:
            self.fail('some files are missing, render failed')
 
