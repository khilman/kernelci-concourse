#!/bin/bash
#set -x

KCI_STORAGE_URL="${KCI_STORAGE_URL:-https://storage.staging.kernelci.org}"

OUT_DIR=${PWD}/monitor-out
mkdir -p ${OUT_DIR}
NEW_COMMITS=${OUT_DIR}/new-commits.txt

cd kernelci-core
if [[ -z "${CONFIG_LIST}" ]]; then
    CONFIG_LIST=$(./kci_build list_configs)
fi    

for config in ${CONFIG_LIST}; do
    commit=$(./kci_build check_new_commit --build-config $config --storage=${KCI_STORAGE_URL})
    if [[ -z ${COMMIT} ]]; then
	echo $config $commit >> ${NEW_COMMITS}
    fi
done

if [[ -s ${NEW_COMMITS} ]]; then
    echo "New commits:"
    cat ${NEW_COMMITS}
fi
