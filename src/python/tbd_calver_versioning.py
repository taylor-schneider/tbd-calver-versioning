from ShellUtilities import Shell
import os
import logging
from pathlib import Path
import sys
# This contains python functions which basically reimpliment the bash script logic
# They make the same exact calls to the git cli and use the same logical structure

def determine_version_number(repo_path=None, adjust_for_pep_440=True):
    
    # Try to run code from the installed path first
    path = Path(sys.executable)
    root_or_drive = path.root or path.drive
    script_name = "determine_tbd_calver_version_number.sh"
    script_path = os.path.join(root_or_drive, "usr", "local", "bin", script_name)
    
    # if the code is not installed, run it from this directory
    if not os.path.exists(script_path):
        logging.warn("Script does not appear to be installed correctly.")
        logging.debug("Running from local path instead.")  
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if not repo_path:
            repo_path = os.getcwd()
        src_root_dir = os.path.dirname(current_dir)
        bash_dir = os.path.join(src_root_dir, "bash", "bin")
        script_path = os.path.join(bash_dir, script_name)
    
    version_number = Shell.execute_shell_command(f"bash {script_path}", cwd=repo_path).Stdout
    
    # With PEP 440 version specifier is `<public identifier>[+<local label>]`
    # This means we need to adjsut our version number to use a + rather than a .
    # for the fourth element in the version number
    
    if adjust_for_pep_440:
        parts = version_number.split(".")
        version_number = ".".join(parts[:3]) + "+" + F"{parts[3]}.{parts[4]}"
    
    return version_number