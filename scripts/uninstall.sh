#!/bin/bash

set -e
set -x

CURRENT_DIR=$(dirname $(realpath $0))
ROOT_DIR=$(dirname $CURRENT_DIR)
SRC_DIR="${ROOT_DIR}/src"
BASH_DIR="${SRC_DIR}/bash"

# Install the scripts
rm -rf /usr/local/repo_inspection
ls "${BASH_DIR}/bin/" | xargs -I {} rm -f "/usr/local/bin/{}"