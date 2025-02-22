import os
import tempfile
from pathlib import Path
import unittest
from promptpack_for_code.core import process_directories, generate_tree

class TestPromptPackForCode(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory structure for testing
        self.test_dir = tempfile.mkdtemp()
        self.root_dir = Path(self.test_dir)
        
        # Create test file structure
        self.create_test_files()
        
    def create_test_files(self):
        # Create directories
        src_dir = self.root_dir / "src"
        src_dir.mkdir()
        utils_dir = src_dir / "utils"
        utils_dir.mkdir()
        
        # Create some test files
        (src_dir / "main.py").write_text("def main():\n    print('Hello')\n")
        (utils_dir / "helper.py").write_text("def helper():\n    return True\n")
        
        # Create file to ignore
        (src_dir / "ignored.pyc").write_text("should not appear")
        
    def tearDown(self):
        # Clean up the temporary directory
        import shutil
        shutil.rmtree(self.test_dir)
        
    def test_generate_tree(self):
        tree = generate_tree(self.root_dir)
        self.assertIn("src", tree)
        self.assertIn("utils", tree)
        self.assertIn("main.py", tree)
        self.assertIn("helper.py", tree)
        self.assertNotIn("ignored.pyc", tree)
        
    def test_process_directories(self):
        output_file = self.root_dir / "output.txt"
        process_directories(
            directories=[str(self.root_dir / "src")],  # 改為列表形式
            root_directory=str(self.root_dir),
            output_file=str(output_file),
            force_overwrite=True
        )
        
        # Check if output file exists
        self.assertTrue(output_file.exists())
        
        # Read the output file
        content = output_file.read_text()
        
        # Check if tree structure is included
        self.assertIn("Project Directory Structure:", content)
        
        # Check if file contents are included with full paths
        self.assertIn("File Contents from Selected Directories:", content)
        self.assertIn("File: src/main.py", content)
        self.assertIn("def main():", content)
        self.assertIn("File: src/utils/helper.py", content)
        self.assertIn("def helper():", content)
        
        # Check if ignored files are excluded
        self.assertNotIn("should not appear", content)

    def test_process_directories_with_custom_ignore(self):
        output_file = self.root_dir / "output.txt"
        process_directories(
            directories=[str(self.root_dir / "src")],  # 改為列表形式
            root_directory=str(self.root_dir),
            output_file=str(output_file),
            ignore_patterns=["*.py"],  # Ignore all Python files
            force_overwrite=True
        )
        
        content = output_file.read_text()
        self.assertNotIn("def main():", content)
        self.assertNotIn("def helper():", content)

    def test_process_multiple_directories(self):
        output_file = self.root_dir / "output.txt"
        process_directories(
            directories=[str(self.root_dir / "src"), str(self.root_dir / "src/utils")],  # 多目錄測試
            root_directory=str(self.root_dir),
            output_file=str(output_file),
            force_overwrite=True
        )
        
        content = output_file.read_text()
        self.assertIn("File: src/main.py", content)
        self.assertIn("File: src/utils/helper.py", content)

if __name__ == '__main__':
    unittest.main()
