# Overview

This repository contains an executable script, and optionally, a python function which deterministically determines the version number of a git repository.

The logic assumes the repository is following the Trunk Based Development branching strategy:

```
Branch Type                                  Branch Flow
==================================================================

release/*                          -------------        --------
                                 /   \       /        /
patch/*                         /      -----         /
                               /                    /
master                    --------------------------------------------
(aka. main, integration)     \ \               /\          /
                              \ \             /  \        /
feature/*                      \  -----------     \      /
                                \                  \    /
bug/*                             ----------------------

```

Each commit in the branch flow will be given a version number based on the CalVer versioning strategy.

```
<year>.<month>.<day>.<branch_type>.<suffix>
```

Integration branches like master and release will use a build number for the suffix. Non-integration branches which can occur in parallel will use the first 7 digits of the commit hash as the suffix.

Examples include:
- 2023.05.23.master.1
- 2022.12.01.feature.f3b24e1


## Requirements
- BASH >= 4.2
- git >= 1.8

## Installation
The scripts can be installed by themselves (i.e. without a python dependency) by running the [install.sh](scripts/install.sh) found in the `scrips/` directory. This script will copy the scripts to the `/usr/local/bin` and the libraries to `/usr/local/<directory-name>` paths.

The python package (and the scripts) can be installed by installing the pip package. The [setup.py](setup.py) is configured to copy the bash scripts to the same place as the `install.sh`. It will also install a python module which hosts a function. Once installed, the module can be imported and the function can be run. The function in turn calls the installed bash scripts.

# Usage
Once installed, simply navigate the current working directory to be inside a git repository and run the bash script or call the python function to determine the version number.

TODO: In a future release a flag will be added to allow inspecting repositories by specifying a path rather than manipulating the CWD.