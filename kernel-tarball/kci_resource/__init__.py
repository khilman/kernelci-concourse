import os
import sys
import errno
import json
import kernelci
import kernelci.build
import kernelci.config.build
import random


def check_new_commit(configs, build_config, storage):
    conf = configs['build_configs'][build_config]
    update = kernelci.build.check_new_commit(conf, storage)
    print(update)
    if update is False or update is True:
        return update


def get_last_commit(configs, build_config, storage):
    conf = configs['build_configs'][build_config]
    commit = kernelci.build.get_last_commit(conf, storage)
    print("get_last_commit = {}".format(commit), file=sys.stderr)
    return commit


class TarballResource:

    def __init__(self, data: dict):
        self.data = json.loads(data)
        self.kci_configs = None
        self.last_commit = None
        self.url = None
        self.kdir = None
        
        if self.data:
            print("data: {}".format(self.data), file=sys.stderr)
        source = self.data.get("source")
        if source:
            self.build_config = source["build_config"]
            self.storage = source["kci_storage_url"]

        kci_core = "/kci/kernelci-core"
        if not os.path.exists(kci_core):
            kci_core = "/home/khilman/work/kernel/ci/kernelci-core"
        build_configs = os.path.join(kci_core,
                                     "config/core/build-configs.yaml")
        if os.path.exists(build_configs):
            self.kci_configs = kernelci.config.build.from_yaml(build_configs)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), build_configs)

    def push(self):
        conf = self.kci_configs['build_configs'][self.build_config]
        func_args = (conf, self.kdir, self.storage, self.api, self.db_token)
        if not all(func_args):
            print("Invalid arguments")
            return False
        tarball_url = kernelci.build.push_tarball(*func_args)
        if not tarball_url:
            return False
        print(tarball_url)
        return True

    def pull(self):
        retries = 1
        tarball = 'linux-src.tar.gz'
        print("pull from URL: {}".format(self.url), file=sys.stderr)
        return kernelci.build.pull_tarball(
            self.kdir, self.url, tarball, retries, False)

    def cmd_check(self, version=None):
        #version = self.data.get("version")
        print("check: version={}".format(version), file=sys.stderr)

        commit = get_last_commit(self.kci_configs,
                                 self.build_config,
                                 self.storage)
        results = {"ref": commit}

        print(json.dumps([results]))

    def cmd_in(self, dest='.'):
        result = dict()
        print("dest={}".format(dest), file=sys.stderr)
        version = self.data.get("version")
        params = self.data.get("params")

        self.kdir = os.path.join(dest, "linux")
        print("KDIR = {}".format(self.kdir), file=sys.stderr)
        
        self.url = params.get("SRC_TARBALL_URL", self.url)
        print("src url = {}".format(self.url), file=sys.stderr)
        ret = self.pull()
        if not ret:
            print("ERROR: pull tarball failed.", file=sys.stderr)
        
        result["version"] = {"ref": self.last_commit}
        print(json.dumps(result))

    def cmd_out(self, dest='.'):
        result = dict()
        print("dest={}".format(dest), file=sys.stderr)

        params = self.data.get("params")
        # if not params:
        #     print(json.dumps(results))

        self.kdir = params["KDIR"]
        self.build_config = params["BUILD_CONFIG"]
        self.storage = params["KCI_STORAGE_URL"]
        self.url = params["SRC_TARBALL_URL"]
        commit = get_last_commit(self.kci_configs,
                                 self.build_config,
                                 self.storage)
        self.last_commit = commit
        result["version"] = {"ref": commit}
        print(json.dumps(result))
