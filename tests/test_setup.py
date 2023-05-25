from ShellUtilities import Shell
import os
from unittest import TestCase

class test_scripts(TestCase):
    
    def test_calling_module_function(self):
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(tests_dir)        
        Shell.execute_shell_command(f"pip install .", cwd=root_dir)
        shell_command = 'python3 -c "import tbd_calver_versioning; print(tbd_calver_versioning.determine_version_number())"'
        Shell.execute_shell_command(shell_command)
        Shell.execute_shell_command(f"pip uninstall -y tbd-calver-versioning-scripts", cwd=root_dir)
