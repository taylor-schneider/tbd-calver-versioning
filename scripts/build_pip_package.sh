#!/bin/bash

set -e
set -x

# By default we will build packages and version them for pypi
if [ -z "${VERSION_FOR_PYPI}" ]; then
    export VERSION_FOR_PYPI=true
fi

python3 -m pip install wheel twine
python3 setup.py sdist bdist_wheel
