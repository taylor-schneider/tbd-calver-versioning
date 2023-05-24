from unittest import TestCase
import tempfile
from ShellUtilities import Shell
import os
import logging
import shutil

logging.basicConfig(level=logging.DEBUG)


class test_determine_tbd_calver_version_number(TestCase):
    
    def _get_repo_directory(self, test_name):
        return os.path.join(tempfile.gettempdir(), test_name)
   
    def _make_tmp_dir(self, test_name):
        tmp_dir = self._get_repo_directory(test_name)
        Shell.execute_shell_command(f"mkdir -p {tmp_dir}")
        self.assertTrue(os.path.exists(tmp_dir))
    
    def _make_repo(self, test_name):
        repo_dir = self._get_repo_directory(test_name)
        Shell.execute_shell_command(f"mkdir -p {repo_dir}")
        Shell.execute_shell_command("git init", cwd=repo_dir)
        Shell.execute_shell_command("git add --all", cwd=repo_dir)
        Shell.execute_shell_command("git commit -m initial checkin", cwd=repo_dir) 
    
    def _get_src_dir(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(tests_dir)
        src_dir = os.path.join(root_dir, "src")
        return src_dir
    
    def _copy_code_files_to_tmp_dir(self, test_name):
        tmp_dir = self._get_repo_directory(test_name)
        Shell.execute_shell_command(f"mkdir -p {tmp_dir}")
        tmp_glob = os.path.join(tmp_dir, "")
        src_dir = self._get_src_dir()
        src_glob = os.path.join(src_dir, "*")        
        Shell.execute_shell_command(f"yes | cp -R {src_glob} {tmp_glob}")
    
    def _cleanup(self, test_name):
        test_dir = self._get_repo_directory(test_name)
        Shell.execute_shell_command("rm -rf {test_dir}")
    
    def test__success(self):
        try:
            self._make_tmp_dir(__name__)
            self._copy_code_files_to_tmp_dir(__name__)
            s = ""
        finally:
            self._cleanup(__name__)
