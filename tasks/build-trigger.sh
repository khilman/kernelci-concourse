#!/bin/bash
#set -x
env

KCI_STORAGE_URL="${KCI_STORAGE_URL:-https://storage.staging.kernelci.org}"
NEW_COMMITS=${PWD}/monitor-out/new-commits.txt

if [[ ! -s ${NEW_COMMITS} ]]; then
    echo "WARNING: No new commits found."
    exit 1
fi

echo "New commits:"
cat ${NEW_COMMITS}
