# test_maya.py 
import os
import shutil
import unittest
from click.testing import CliRunner
from maya_cli.cli import maya
from maya_cli.project_generator import PROJECT_STRUCTURE

test_project_name = "test_ai_project"

def project_exists(base_path, structure):
    """ Recursively check if project structure exists """
    for folder in structure.keys():
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            return False
        if isinstance(structure[folder], dict) and not project_exists(folder_path, structure[folder]):
            return False
    return True

class TestMayaCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
    
    def tearDown(self):
        if os.path.exists(test_project_name):
            shutil.rmtree(test_project_name)
    
    def test_create_project(self):
        result = self.runner.invoke(maya, ["create", test_project_name])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(f"✅ AI project '{test_project_name}' created successfully!", result.output)
        self.assertTrue(project_exists(test_project_name, PROJECT_STRUCTURE))
    
    def test_create_existing_project(self):
        os.makedirs(test_project_name, exist_ok=True)
        result = self.runner.invoke(maya, ["create", test_project_name])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(f"Error: Project '{test_project_name}' already exists.", result.output)
        
if __name__ == "__main__":
    unittest.main()