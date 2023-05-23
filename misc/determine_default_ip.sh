#!/bin/bash

set -e
set -x

DEFAULT_NIC=$(ip -o route get to $(route -nv | grep -E '^0.0.0.0' | awk '{print $2}') | awk '{print $3}')
DEFAULT_IP=$(ip addr show $DEFAULT_NIC | grep "inet " | awk '{print $2}' | awk -F/ '{print $1}')

echo "${DEFAULT_IP}"
