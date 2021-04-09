import os
import sys
import errno
import json
import pprint
import kernelci
import kernelci.build
import kernelci.config.build


class TarballResource:

    def __init__(self, data: dict):
        self.data = json.loads(data)
        self.kci_configs = None
        if self.data:
            print(json.dumps(self.data, indent=2), file=sys.stderr)
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

    def pull(self, kdir, url):
        retries = 1
        tarball = 'linux-src.tar.gz'
        print("pull from URL: {}".format(url), file=sys.stderr)
        return kernelci.build.pull_tarball(
            kdir, url, tarball, retries, False)

    def get_last_commit(self):
        conf = self.kci_configs['build_configs'][self.build_config]
        commit = kernelci.build.get_last_commit(conf, self.storage)
        print("last_commit = {}".format(commit), file=sys.stderr)
        return commit
    
    def cmd_check(self, version=None):
        print("CHECK: version={}".format(version), file=sys.stderr)
        commit = self.get_last_commit()
        results = {
            "ref": commit,
            "describe": "",
            "url": "",
        }
        print(json.dumps([results]))

    def cmd_in(self, dest='.'):
        result = dict()
        print("IN: dest={}".format(dest), file=sys.stderr)
        version = self.data.get('version')
            
        kdir = os.path.join(dest, "linux")
        url = version.get('url')
        ret = self.pull(kdir, url)
        if not ret:
            print("ERROR: pull tarball failed.", file=sys.stderr)
        
        result["version"] = version
        print(json.dumps(result))

    def cmd_out(self, dest='.'):
        result = dict()
        print("OUT: dest={}".format(dest), file=sys.stderr)

        params = self.data.get("params")
        url = params.get("SRC_TARBALL_URL")
        commit = params.get("COMMIT")
        last_commit = self.get_last_commit()
        if commit != last_commit:
            print("ERROR: commit:{} != last_comit:{}".format(
                commit, last_commit), file=sys.stderr)
            return
        
        result["version"] = {
            "ref": commit,
            "describe": params.get("DESCRIBE"),
            "url": url,
        }
        result["metadata"] = [
            {"name": "build_config",
             "value": self.build_config},
            {"name": url,
             "value": params.get("SRC_TARBALL_URL")},
            {"name": "commit",
             "value": params.get("COMMIT")},
            {"name": "describe",
             "value": params.get("DESCRIBE")},
            {"name": "describe_v",
             "value": params.get("DESCRIBE_V")},
        ]
        print(json.dumps(result))
