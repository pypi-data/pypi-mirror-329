import unittest
import subprocess
import os
import tempfile
import shutil
import pathlib
import filecmp

def are_dirs_equal(dir1, dir2):
    """
    Compare two directories recursively to check if they contain the same files with the same content.
    """
    dcmp = filecmp.dircmp(dir1, dir2)
    if dcmp.left_only or dcmp.right_only or dcmp.diff_files:
        return False
    for common_dir in dcmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not are_dirs_equal(new_dir1, new_dir2):
            return False
    return True

class TestGitAndTillyCommands(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.tilly_dir = pathlib.Path(__file__).parent.parent

        os.chdir(self.test_dir)
        print("test dir created at", self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_git_and_til_script(self):
        # Write the shell script to the test directory
        script_content = f"""#!/bin/bash
set -e
git init
mkdir example
echo "# My first TIL with tilly" > example/first-til.md
git add .
# commit with a fixed date
GIT_AUTHOR_DATE="2024-07-07T12:00:00Z" GIT_COMMITTER_DATE="2024-07-07T12:00:00Z" git commit -m "adding first til"
uv venv .venv
source .venv/bin/activate
uv pip install -e {self.tilly_dir}
tilly build
tilly gen-static
"""

        with open("setup_til.sh", "w") as f:
            f.write(script_content)

        # Make the script executable
        subprocess.run(["chmod", "+x", "setup_til.sh"], check=True)

        # Run the script
        subprocess.run(["./setup_til.sh"], check=True, capture_output=True, text=True)

        # Assertions to check if the script did what it was supposed to
        # Check if git repo was initialized
        self.assertTrue(os.path.exists(".git"))

        # Check if venv was created
        self.assertTrue(os.path.exists(".venv"))

        # Check if the directory was created
        self.assertTrue(os.path.isdir("example"))

        # Check if the file was created
        self.assertTrue(os.path.isfile("example/first-til.md"))

        # Check file content
        with open("example/first-til.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "# My first TIL with tilly\n")

        # Check if tils.db was creatd
        self.assertTrue(os.path.isfile("tils.db"))

        # check if generated html is equal to fixtures
        static_files_folder = pathlib.Path(self.test_dir) / "_static"
        fixtures_folder = self.tilly_dir / "test" / "fixtures"
        # update fixtures:
        # shutil.copytree(static_files_folder, fixtures_folder, dirs_exist_ok=True)
        self.assertTrue(are_dirs_equal(static_files_folder, fixtures_folder), "Directories do not match")

if __name__ == '__main__':
    unittest.main()