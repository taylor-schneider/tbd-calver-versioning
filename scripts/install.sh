#!/bin/bash

set -e
set -x

CURRENT_DIR=$(dirname $(realpath $0))
ROOT_DIR=$(dirname $CURRENT_DIR)
SRC_DIR="${ROOT_DIR}/src"
BASH_DIR="${SRC_DIR}/bash"

# Install the scripts
cp -R ${BASH_DIR}/repo_inspection "/usr/local/"
ls "${BASH_DIR}/bin/" | xargs -I {} cp "${BASH_DIR}/bin/{}" /usr/local/bin/