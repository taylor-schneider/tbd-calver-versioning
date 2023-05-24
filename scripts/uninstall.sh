#!/bin/bash

set -e

# This script will uninstall the software that was previously installed

CURRENT_DIR=$(dirname $(realpath $0))
ROOT_DIR=$(dirname $CURRENT_DIR)
SRC_DIR="${ROOT_DIR}/src"

INSTALL_DIR=(/usr/local/tbd_calver_versioning)

rm -rf "${INSTALL_DIR}"

if [ -f "/usr/local/bin/determine_tbd_calver_version_number.sh" ]; then
    rm -f /usr/local/bin/determine_tbd_calver_version_number.sh
fi