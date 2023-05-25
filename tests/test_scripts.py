from ShellUtilities import Shell
import os
from unittest import TestCase

class test_scripts(TestCase):
    def test_install(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(tests_dir)
        scripts_dir = os.path.join(root_dir, "scripts")
        install_script_path = os.path.join(scripts_dir, "install.sh")
        Shell.execute_shell_command(f"bash {install_script_path}")
        script_path = "/usr/local/bin/determine_tbd_calver_version_number.sh"
        self.assertTrue(os.path.exists(script_path))
        version_number = Shell.execute_shell_command(f"bash {script_path}")
        self.assertIsNotNone(version_number)
     
    def test_uninstall(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(tests_dir)
        scripts_dir = os.path.join(root_dir, "scripts")
        install_script_path = os.path.join(scripts_dir, "uninstall.sh")
        Shell.execute_shell_command(f"bash {install_script_path}")
        script_path = "/usr/local/bin/determine_tbd_calver_version_number.sh"
        self.assertFalse(os.path.exists(script_path))
        self.assertFalse(os.path.exists("/usr/local/share/repo_inspection"))
