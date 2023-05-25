import sys
import setuptools
import os
import logging

logging.basicConfig(level=logging.DEBUG, filename="/tmp/foobar.log")

# Read the text from the README
with open('README.md', "r") as fh:
    long_description = fh.read()

# Read the text from the requirements file
with open('requirements.txt') as file:
    lines = file.readlines()
    install_requires = [line.rstrip() for line in lines]   

# Set the directory for the source code to be installed
source_code_dir = "src/python"

# The data_files functionality allows us to copy files into to the /usr/local directory
# We will provide a dictionary with relative destination path and the contents from the local path

def get_data_paths_for_bash_files(source_code_dir):
    bash_files = {}
    for reletive_directory_path, sub_directories, files in os.walk(source_code_dir):
        for file in files:
            # Files in the root are going to the bin directory
            if reletive_directory_path == source_code_dir:
                if "bin" not in bash_files.keys():
                   bash_files["bin"] = [] 
                bash_files["bin"].append(os.path.join(reletive_directory_path, file))
            # Files in subdirectories will be mapped accordingly
            else:
                rel_usr_share_dir = os.path.relpath(reletive_directory_path, source_code_dir)
                if rel_usr_share_dir not in bash_files.keys():
                   bash_files[rel_usr_share_dir] = [] 
                bash_files[rel_usr_share_dir].append(os.path.join(reletive_directory_path, file))
    # Now that we have the information we need to transform it
    bash_files = [(key, value) for key,value in bash_files.items()]    
    return bash_files  
import json
bash_files = get_data_paths_for_bash_files("src/bash")
logging.debug(json.dumps(bash_files, indent=4))


# Run the setuptools setup function to install our code
package_name = "tbd-calver-versioning-scripts"
setuptools.setup(
    name=package_name,
    version="1.0.0",
    author="tschneider",
    author_email="tschneider@live.com",
    description="A set of tools to manage a code repository using trunk based development and CalVer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(source_code_dir),
    py_modules=[
        "src/python/tbd_calver_versioning"
    ],
    install_requires= install_requires,
    data_files = bash_files,
    classifiers=[
        "Programming Language :: Python :: BASH",
        "Programming Language :: Python :: 3",
        "LICENSE :: OSI APPROVED :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)",
        "Operating System :: OS Independent",
    ],
)