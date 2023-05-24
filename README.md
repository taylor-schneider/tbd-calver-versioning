# Overview

This repository contains an executable script, and accompanying library, which deterministically determines the version number of a git repository.

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