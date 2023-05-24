#!/bin/bash

set -e
set -x

# This script will install the software contained in this repository
# It will also create a symlink in the /usr/local/bin directory

CURRENT_DIR=$(dirname $(realpath $0))
ROOT_DIR=$(dirname $CURRENT_DIR)
SRC_DIR="${ROOT_DIR}/src"

INSTALL_DIR=(/usr/local/tbd_calver_versioning)

mkdir -p "${INSTALL_DIR}"

yes | cp -R ${SRC_DIR}/* "${INSTALL_DIR}"

if [ -f "/usr/local/bin/determine_tbd_calver_version_number.sh" ]; then
    rm -f /usr/local/bin/determine_tbd_calver_version_number.sh
fi

ln -s /usr/local/tbd_calver_versioning/determine_tbd_calver_version_number.sh /usr/local/bin/determine_tbd_calver_version_number.sh