from unittest import TestCase
import tempfile
from ShellUtilities import Shell, ShellCommandException
import os
import logging
import shutil
import datetime
import tbd_calver_versioning

logging.basicConfig(level=logging.DEBUG)


class test_determine_tbd_calver_version_number(TestCase):

    # ===========================================
    # Functions related to paths and directories
    # ===========================================

    def _get_repo_directory(self, test_name):
        return os.path.join(tempfile.gettempdir(), test_name)
   
    def _make_tmp_dir(self, test_name):
        tmp_dir = self._get_repo_directory(test_name)
        Shell.execute_shell_command(f"mkdir -p {tmp_dir}")
        self.assertTrue(os.path.exists(tmp_dir))
        return tmp_dir
    
    def _get_src_dir(self):
        module_dir = os.path.dirname(os.path.abspath(__file__))
        tests_dir = os.path.dirname(module_dir)
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
        Shell.execute_shell_command(f"rm -rf {test_dir}")
        self.assertFalse(os.path.exists(test_dir))
    
    # ============================================
    # Functions related to git
    # ============================================
    
    def _make_commit(self, test_name):
        repo_dir = self._get_repo_directory(test_name)
        Shell.execute_shell_command("git add --all", cwd=repo_dir)
        Shell.execute_shell_command("git commit -m 'making a commit'", cwd=repo_dir) 
    
    def _make_repo(self, test_name):
        repo_dir = self._get_repo_directory(test_name)
        Shell.execute_shell_command(f"mkdir -p {repo_dir}")
        Shell.execute_shell_command("git init", cwd=repo_dir)
        self._make_commit(test_name)
    
    def _create_branch(self, test_name, branch_name):
        repo_dir = self._get_repo_directory(test_name)
        Shell.execute_shell_command(f"git checkout -b {branch_name}", cwd=repo_dir)

    def _checkout_branch(self, test_name, branch_name):
        repo_dir = self._get_repo_directory(test_name)
        Shell.execute_shell_command(f"git checkout {branch_name}", cwd=repo_dir)

    def _get_commit_hash(self, test_name):
        repo_dir = self._get_repo_directory(test_name)
        return Shell.execute_shell_command("git rev-parse HEAD", cwd=repo_dir).Stdout

    def _merge_branch(self, test_name, source_branch):
        repo_dir = self._get_repo_directory(test_name)
        Shell.execute_shell_command(f"git merge --no-ff -m 'Merge message' {source_branch}", cwd=repo_dir)

    # ============================================
    # Functions for running scripts in the src/ dir
    # ============================================  

    def _determine_tbd_calver_version_number(self, test_name):
        tmp_dir = self._get_repo_directory(test_name)
        return tbd_calver_versioning.determine_version_number(tmp_dir)

    # ============================================
    # Test Functions
    # ============================================

    def test__success__script_called_from_repo(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            expected_version = f"{date}+master.1"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)

    def test__success__script_called_from_repo_without_pep_440(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            version = tbd_calver_versioning.determine_version_number(tmp_dir, adjust_for_pep_440=False)
            date = str(datetime.date.today()).replace("-", ".")
            expected_version = f"{date}.master.1"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)