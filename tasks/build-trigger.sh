#!/bin/bash
env
set -x

KDIR=$PWD/kernel-repo
echo "BUILD_CONFIG: $BUILD_CONFIG"

cd kernelci-core

# config already built?
NEW_COMMIT=$(./kci_build check_new_commit --build-config $BUILD_CONFIG --storage $KCI_STORAGE_URL)
if [[ -z $NEW_COMMIT ]]; then
    exit 0
fi

(cd $KDIR; ls -l; ls -l .git; git describe)
ls -l .git
./kci_build describe --build-config $BUILD_CONFIG --kdir $KDIR
