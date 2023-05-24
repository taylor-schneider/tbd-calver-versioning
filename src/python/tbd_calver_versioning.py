from ShellUtilities import Shell
import os


# This contains python functions which basically reimpliment the bash script logic
# They make the same exact calls to the git cli and use the same logical structure

def determine_version_number(repo_path=None):
    
    # Try to run code from the installed path first
    script_name = "determine_tbd_calver_version_number.sh"
    script_path = os.path.join("usr", "local", "bin", script_name)
    
    # if the code is not installed, run it from this directory
    if not os.path.exists(script_path):     
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if not repo_path:
            repo_path = os.getcwd()
        src_root_dir = os.path.dirname(current_dir)
        bash_dir = os.path.join(src_root_dir, "bash", "bin")
        script_path = os.path.join(bash_dir, script_name)
    
    return Shell.execute_shell_command(f"bash {script_path}", cwd=repo_path).Stdout