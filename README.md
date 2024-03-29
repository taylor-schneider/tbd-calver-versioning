# Overview

This repository contains several useful components:
1. A [BASH script](src/bash/bin/determine_tbd_calver_version_number.sh) which determines the version number of a git repository
2. A [python module](src/python/tbd_calver_versioning.py) which contains a function which calls the BASH script and then produces a PEP440 compliant version number.
3. Scripts to [install](scripts/install.sh)/[uninstall](scripts/uninstall.sh) the BASH script, and accompanying libraries, to `/usr/local/bin`
4. A [setup.py](setup.py) allowing this project to be installed as a pip package
5. A [pyproject.toml](pyproject.toml) which will install prerequisite packages (ShellUtilities) before running the setup.py.
6. An [example Setup.py](tests/dummy_files/setup.py) and [example pyproject.toml](tests/dummy_files/pyproject.toml) showing how a function in this python library can be called to version a package automatically as part of another project's setup.py.


# Versioning

The version number follows the [CalVer](https://calver.org/) versioning scheme. Each version consists of 5 parts:
- **Major** - Year of the commit
- **Minor** - Month of the commit
- **Micro** - Day of the commit
- **Modifier** - Branch and either commit hash or build number

The version number will thus be as follows:

```
<year>.<month>.<day>.<branch_type>.<commit_hash_or_build_number>
```

**Note**: For the PEP440 standard compliance, the python function will return a version number as follows (notice the '+'):

```
<year>.<month>.<day>+<branch_type>.<commit_hash_or_build_number>
```

The logic to construct the version number assumes the repository is following the Trunk Based Development branching strategy:

```
Branch Type                                  Branch Flow
==================================================================

release/*                          -------------          ----------
                                 /   \       /          /      / 
patch/*                         /      -----           /      /
                               /             \        /      /
master                    --------------------------------------------
(aka. main, integration)     \ \                 /\          /
                              \ \               /  \        /
feature/*                      \  --------------    \      /
                                \                    \    /
bug/*                             ------------------------

```

Each commit in the branch flow will be given a version number based on the CalVer versioning strategy.

Integration branches like master and release will use a build number for the suffix. Non-integration branches which can occur in parallel will use the first 7 digits of the commit hash as the suffix.

Examples include:
- 2023.05.23.master.1
- 2022.12.01.feature.f3b24e1

### Note On Merging
When merging a non-integration branch into an integration branch we must ensure that there is a merge commit. If we allow the branch to simply fast forward, the logic for determining the version number cannot work. This is because a "branch" is simply a version history and if the version histories are identical between two branches, then our logic breaks. To fix this, use the --no-ff to force a merge commit. For example, if merging main up into a release branch, us the --no-ff to ensure a new merge commit is created on the release and guarantee the release number will be incremented properly.

## Requirements
- BASH >= 4.2
- git >= 1.8

## Installation
There are two options for installing the utilities in this repository:
- bash scripts only (no python dependency)
- python module and bash scipts

The bash scripts can be installed by themselves (i.e. without a python dependency) by running the [install.sh](scripts/install.sh) found in the `scrips/` directory of this repository. This script will copy the scripts from the git repo to the `/usr/local/bin` and the libraries to `/usr/local/<directory-name>` paths.

The python package (and the scripts) can be installed by installing the pip package. The [setup.py](setup.py) is configured to copy the bash scripts to the same place as the `install.sh`. It will also install a python module which hosts a function. Once installed, the module can be imported and the function can be run. The function in turn calls the installed bash scripts.

**NOTE**: If using conda, the bin path will automagically change to a conda env path. As such the paths of the installed scripts may differ depending on whether one used the install.sh or the pip install method.

# Usage
Once installed, simply navigate the current working directory to be inside a git repository and run the bash script or call the python function to determine the version number for that repository.

# TODO
- repo-flag: add a flag to allow inspecting repositories by specifying a path rather than manipulating the CWD.