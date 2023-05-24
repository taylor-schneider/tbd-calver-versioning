import sys
import setuptools

# Read the text from the README
with open('README.md', "r") as fh:
    long_description = fh.read()

# Read the text from the requirements file
with open('requirements.txt') as file:
    lines = file.readlines()
    install_requires = [line.rstrip() for line in lines]   

# Set the directory for the source code to be installed
source_code_dir = "src"

# Run the setuptools setup function to install our code
setuptools.setup(
    name="tbd-calver-versioning-scripts",
    version="1.0.0",
    author="tschneider",
    author_email="tschneider@live.com",
    description="A set of tools to manage a code repository using trunk based development and CalVer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(source_code_dir),
    package_dir={
        "": source_code_dir
    },
    install_requires= install_requires,
    classifiers=[
        "Programming Language :: Python :: BASH",
        "Programming Language :: Python :: 3",
        "LICENSE :: OSI APPROVED :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)",
        "Operating System :: OS Independent",
    ],
)