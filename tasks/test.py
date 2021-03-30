#!/usr/bin/env python3
import sys

# HACK: needed when using a local checkout of kernelci
import os
os.chdir("kernelci-core")
sys.path.append(os.getcwd())

import kernelci
import kernelci.build
import kernelci.config.build

configs = kernelci.config.build.from_yaml("config/core/build-configs.yaml")
config_list = os.environ("CONFIG_LIST")
if config_list:
    config_list = "$(params.CONFIG_LIST)".split()
else:
    config_list = list(configs['build_configs'].keys())

with open("$(results.config-list.path)", "w") as file:
    for conf_name in config_list:
        conf = configs['build_configs'][conf_name]
        update = kernelci.build.check_new_commit(conf,
                                                 "$(params.KCI_STORAGE_URL)")

        if type(update) != bool:
            file.write("{}\n".format(conf_name))
            print("New commit in {}: {}".format(conf_name, update))
