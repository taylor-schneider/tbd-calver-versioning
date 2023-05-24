from unittest import TestCase
import tempfile
from ShellUtilities import Shell, ShellCommandException
import os
import logging
import shutil
import datetime

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
        script_path = os.path.join(self._get_src_dir(), "versioning", "determine_tbd_calver_version_number.sh")
        result = Shell.execute_shell_command(f"bash {script_path}", cwd=tmp_dir)
        version = result.Stdout.split(os.linesep)[0]
        return version

    # ============================================
    # Test Functions
    # ============================================

    def test__success__commit_to_master(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            expected_version = f"{date}.master.1"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)
            
    def test__success__commit_to_master_twice(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            Shell.execute_shell_command(f"echo 'blah' > {dummy_file}")
            self._make_commit(__name__)
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            expected_version = f"{date}.master.2"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)

    def test__success__commit_to_feature(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            self._create_branch(__name__, "feature/testing-a-thing")
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            commit_hash = self._get_commit_hash(__name__)
            expected_version = f"{date}.feature.{commit_hash[:7]}"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)
  
    def test__success__commit_to_bug(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            self._create_branch(__name__, "bug/testing-a-thing")
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            commit_hash = self._get_commit_hash(__name__)
            expected_version = f"{date}.bug.{commit_hash[:7]}"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)
  
    def test__failure__commit_to_unsupported_branch_type(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            self._create_branch(__name__, "unsupporded/testing-a-thing")
            with self.assertRaises(Exception) as context:
                version = self._determine_tbd_calver_version_number(__name__)
            self.assertEqual(1, context.exception.__cause__.ExitCode)
            err_msg = 'The branch type unsupporded is not supported'
            self.assertEqual(err_msg, context.exception.__cause__.Stdout)
            self.assertIsNotNone(context.exception.__cause__.Stderr)
        finally:
            self._cleanup(__name__)

    def test__success__merge_feature_into_master(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            self._create_branch(__name__, "feature/testing-a-thing")
            Shell.execute_shell_command(f"echo 'blah' > {dummy_file}")
            self._make_commit(__name__)
            self._checkout_branch(__name__, "master")
            self._merge_branch(__name__,"feature/testing-a-thing")
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            expected_version = f"{date}.master.2"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)

    def test__success__merge_two_features_into_master(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            # create first branch and merge
            self._create_branch(__name__, "feature/testing-a-thing")
            Shell.execute_shell_command(f"echo 'blah' > {dummy_file}")
            self._make_commit(__name__)
            self._checkout_branch(__name__, "master")
            self._merge_branch(__name__,"feature/testing-a-thing")
            # create second branch and berge
            self._create_branch(__name__, "feature/testing-another-thing")
            Shell.execute_shell_command(f"echo 'foobar blah' > {dummy_file}")
            self._make_commit(__name__)
            self._checkout_branch(__name__, "master")
            self._merge_branch(__name__,"feature/testing-another-thing")
            # Check the version numebr
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            expected_version = f"{date}.master.3"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)

    def test__success__cut_a_release(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            self._create_branch(__name__, "release/releasing-a-thing")
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            commit_hash = self._get_commit_hash(__name__)
            expected_version = f"{date}.release.1"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)

    def test__success__create_a_patch(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            self._create_branch(__name__, "release/releasing-a-thing")
            self._create_branch(__name__, "patch/pathing-a-thing")
            Shell.execute_shell_command(f"echo 'blah' > {dummy_file}")
            self._make_commit(__name__)
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            commit_hash = self._get_commit_hash(__name__)
            expected_version = f"{date}.patch.{commit_hash[:7]}"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)
  
    def test__success__patch_a_release(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            self._create_branch(__name__, "release/releasing-a-thing")
            self._create_branch(__name__, "patch/pathing-a-thing")
            Shell.execute_shell_command(f"echo 'blah' > {dummy_file}")
            self._make_commit(__name__)
            self._checkout_branch(__name__, "release/releasing-a-thing")
            self._merge_branch(__name__, "patch/pathing-a-thing")
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            commit_hash = self._get_commit_hash(__name__)
            expected_version = f"{date}.release.2"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)

    def test__success__patch_a_release_twice(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            self._create_branch(__name__, "release/releasing-a-thing")
            self._create_branch(__name__, "patch/pathing-a-thing")
            Shell.execute_shell_command(f"echo 'blah' > {dummy_file}")
            self._make_commit(__name__)
            Shell.execute_shell_command(f"echo 'blah blach' > {dummy_file}")
            self._make_commit(__name__)
            self._checkout_branch(__name__, "release/releasing-a-thing")
            self._merge_branch(__name__, "patch/pathing-a-thing")
            self._create_branch(__name__, "patch/pathing-another-thing")
            Shell.execute_shell_command(f"echo 'blah' > {dummy_file}")
            self._make_commit(__name__)
            Shell.execute_shell_command(f"echo 'blah blach' > {dummy_file}")
            self._make_commit(__name__)
            self._checkout_branch(__name__, "release/releasing-a-thing")
            self._merge_branch(__name__, "patch/pathing-another-thing")
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            commit_hash = self._get_commit_hash(__name__)
            expected_version = f"{date}.release.3"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)
 
    def test__success__patch_a_release_twice_and_merge_to_main(self):
        try:
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            self._create_branch(__name__, "release/releasing-a-thing")
            self._create_branch(__name__, "patch/pathing-a-thing")
            Shell.execute_shell_command(f"echo 'blah' > {dummy_file}")
            self._make_commit(__name__)
            Shell.execute_shell_command(f"echo 'blah blach' > {dummy_file}")
            self._make_commit(__name__)
            self._checkout_branch(__name__, "release/releasing-a-thing")
            self._merge_branch(__name__, "patch/pathing-a-thing")
            self._create_branch(__name__, "patch/pathing-another-thing")
            Shell.execute_shell_command(f"echo 'blah' > {dummy_file}")
            self._make_commit(__name__)
            Shell.execute_shell_command(f"echo 'blah blach' > {dummy_file}")
            self._make_commit(__name__)
            self._checkout_branch(__name__, "release/releasing-a-thing")
            self._merge_branch(__name__, "patch/pathing-another-thing")
            version = self._determine_tbd_calver_version_number(__name__)
            date = str(datetime.date.today()).replace("-", ".")
            commit_hash = self._get_commit_hash(__name__)
            expected_version = f"{date}.release.3"
            # Now merge the patches to main
            self._checkout_branch(__name__, "master")
            self._merge_branch(__name__, "patch/pathing-a-thing")
            version = self._determine_tbd_calver_version_number(__name__)
            expected_version = f"{date}.master.2"
            self.assertEqual(expected_version, version)
            self._merge_branch(__name__, "patch/pathing-another-thing")
            version = self._determine_tbd_calver_version_number(__name__)
            expected_version = f"{date}.master.3"
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)

    # ============================================
    # Test Functions - for wierd situations
    # ============================================

    def test__success__merge_feature_into_feture_then_main(self):
        try:
            # Create the repo
            tmp_dir = self._make_tmp_dir(__name__)
            dummy_file = os.path.join(tmp_dir, "foobat.txt")
            Shell.execute_shell_command(f"echo 'foobar' > {dummy_file}")
            self._make_repo(__name__)
            # create the feature
            self._create_branch(__name__, "feature/testing-a-thing")
            Shell.execute_shell_command(f"echo 'blah' > {dummy_file}")
            self._make_commit(__name__)
            # Create the 2nd feature
            self._create_branch(__name__, "feature/branching-off-feature")
            Shell.execute_shell_command(f"echo 'blah blah' > {dummy_file}")
            self._make_commit(__name__)
            # Merge the feature into the feature
            self._checkout_branch(__name__, "feature/testing-a-thing")
            self._merge_branch(__name__, "feature/branching-off-feature")
            # Check the version numbers
            date = str(datetime.date.today()).replace("-", ".")
            commit_hash = self._get_commit_hash(__name__)
            expected_version = f"{date}.feature.{commit_hash[:7]}"
            version = self._determine_tbd_calver_version_number(__name__)
            self.assertEqual(expected_version, version)
            # Merge into master
            self._checkout_branch(__name__, "master")
            self._merge_branch(__name__, "feature/testing-a-thing")
            # Check the version numbers
            date = str(datetime.date.today()).replace("-", ".")
            expected_version = f"{date}.master.2"
            version = self._determine_tbd_calver_version_number(__name__)
            self.assertEqual(expected_version, version)
        finally:
            self._cleanup(__name__)

