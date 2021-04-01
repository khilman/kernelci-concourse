#!/usr/bin/env python3
import sys

# HACK: needed when using a local checkout of kernelci
import os
kci_core_path = os.path.join(os.getcwd(), "kernelci-core")
sys.path.append(kci_core_path)
import kernelci
import kernelci.build
import kernelci.config.build

configs = kernelci.config.build.from_yaml(
    kci_core_path + "/config/core/build-configs.yaml")

config_list = os.environ.get("CONFIG_LIST", "").split()
if config_list:
    pass
else:
    config_list = list(configs['build_configs'].keys())

out_dir = "monitor-out"
try:
    os.mkdir(out_dir)
except FileExistsError:
    pass

with open(os.path.join(os.path.join(out_dir, "config-list.txt")), "w") as file:
    for conf_name in config_list:
        conf = configs['build_configs'][conf_name]
        update = kernelci.build.check_new_commit(
            conf, os.environ.get("KCI_STORAGE_URL"))

        if type(update) != bool:
            file.write("{}\n".format(conf_name))
            print("New commit in {}: {}".format(conf_name, update))
