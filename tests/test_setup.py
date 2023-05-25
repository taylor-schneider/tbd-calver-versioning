from ShellUtilities import Shell
import os
from unittest import TestCase
import tempfile


class test_scripts(TestCase):
    
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

    # ===========================================
    # Test Functions
    # ===========================================

    def test_calling_module_function_from_cli(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(tests_dir)        
        Shell.execute_shell_command(f"pip install .", cwd=root_dir)
        shell_command = 'python3 -c "import tbd_calver_versioning; print(tbd_calver_versioning.determine_version_number())"'
        Shell.execute_shell_command(shell_command)
        Shell.execute_shell_command(f"pip uninstall -y tbd-calver-versioning", cwd=root_dir)

    def test_calling_module_function_from_setup_py(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(tests_dir)  
        repo_dir = self._make_tmp_dir(__name__)
        try:
            # Install the module      
            Shell.execute_shell_command(f"pip install .", cwd=root_dir)
            shell_command = 'python3 -c "import tbd_calver_versioning; print(tbd_calver_versioning.determine_version_number())"'
            a = Shell.execute_shell_command(shell_command)
            # Create the dummy project
            dummy_setup_py = os.path.join(tests_dir, "dummy_files", "setup.py")
            Shell.execute_shell_command(f"cp {dummy_setup_py} {repo_dir}/")
            src_dir = os.path.join(repo_dir, 'src')
            Shell.execute_shell_command(f"mkdir {src_dir}")
            Shell.execute_shell_command(f"echo 'print(\"Hello, World!\")' > {src_dir}/test.py")
            Shell.execute_shell_command(f"touch {src_dir}/__init__.py")
            self._make_repo(__name__)
            # Ensure the project can still be imported
            b = Shell.execute_shell_command(shell_command)
            c = Shell.execute_shell_command(shell_command, cwd=repo_dir)
            # Install the dummy project
            Shell.execute_shell_command("pip install .", cwd=repo_dir)


            # Ensure the correct version was installed
            package_name = "DummyPackage"
            result = Shell.execute_shell_command(r"pip list | grep " + package_name +" | awk '{print $2}'")
            installed_version = result.Stdout.split(os.linesep)[0]
            self.assertIsNotNone(installed_version)
        finally:
            # Cleanup
            Shell.execute_shell_command(f"pip uninstall -y DummyPackage", cwd=root_dir)
            Shell.execute_shell_command(f"pip uninstall -y tbd-calver-versioning", cwd=root_dir)
            Shell.execute_shell_command(f"rm -rf {repo_dir}")
