#!/bin/bash

set -e
set -x

# By default we will build packages and version them for pypi
if [ -z "${VERSION_FOR_PYPY}" ]; then
    VERSION_FOR_PYPY=true
fi

python3 -m pip install wheel twine
python3 setup.py sdist bdist_wheel
